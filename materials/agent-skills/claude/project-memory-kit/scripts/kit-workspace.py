"""Kit worktree preflight. No workspace or MCP configuration is created by status.

This is intentionally Git-only: AOCI remains an optional, separately updated MCP.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def git(repo: Path, *args: str, check: bool = False) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if check and result.returncode:
        raise ValueError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result


def root_of(repo: Path) -> Path:
    if not repo.is_dir():
        raise ValueError("repository directory does not exist")
    result = git(repo, "rev-parse", "--show-toplevel", check=True)
    return Path(result.stdout.strip()).resolve()


def checkout_kind(root: Path) -> str:
    git_dir = git(root, "rev-parse", "--absolute-git-dir", check=True).stdout.strip()
    common = git(root, "rev-parse", "--git-common-dir", check=True).stdout.strip()
    common_path = Path(common)
    if not common_path.is_absolute():
        common_path = root / common_path
    return "clone" if Path(git_dir).resolve() == common_path.resolve() else "worktree"


def status(repo: Path, mode: str, integration_branch: str | None) -> dict[str, object]:
    root = root_of(repo)
    branch_result = git(root, "symbolic-ref", "--quiet", "--short", "HEAD")
    branch = branch_result.stdout.strip() if branch_result.returncode == 0 else None
    kind = checkout_kind(root)
    if mode == "single":
        state = "ready" if branch else "needs_branch"
    elif not integration_branch:
        state = "needs_integration_branch"
    elif not branch:
        state = "needs_branch"
    elif branch == integration_branch:
        state = "needs_workspace"
    else:
        state = "ready"
    return {
        "status": state,
        "repo": str(root),
        "checkout_kind": kind,
        "branch": branch,
        "mode": mode,
        "integration_branch": integration_branch,
        "creation_required": state == "needs_workspace",
        "concurrent_writer_exclusivity_proven": False,
        "message": "Git cannot prove another Agent is not writing this checkout; coordinate exclusive use.",
    }


def create(repo: Path, target: Path, branch: str, base: str, integration_branch: str) -> dict[str, object]:
    root = root_of(repo)
    if not target.is_absolute():
        raise ValueError("target must be an explicit absolute path")
    resolved = target.resolve()
    if resolved.exists():
        raise ValueError("target already exists; refusing to reuse or overwrite")
    if not resolved.parent.is_dir():
        raise ValueError("target parent directory does not exist")
    if resolved == root or resolved.is_relative_to(root):
        raise ValueError("target must be outside the source checkout")
    if not branch or branch == integration_branch:
        raise ValueError("new branch must differ from the integration branch")
    git(root, "check-ref-format", "--branch", branch, check=True)
    if git(root, "show-ref", "--verify", "--quiet", f"refs/heads/{branch}").returncode == 0:
        raise ValueError("branch already exists; use its existing worktree instead")
    git(root, "rev-parse", "--verify", f"{base}^{{commit}}", check=True)
    if git(root, "status", "--porcelain", "--untracked-files=no", check=True).stdout.strip():
        raise ValueError("source checkout has tracked modifications; stabilize it before creating a worktree")
    git(root, "worktree", "add", "-b", branch, str(resolved), base, check=True)
    return {
        "status": "created",
        "repo": str(resolved),
        "branch": branch,
        "base": base,
        "aoci_setup_required_if_enabled": True,
        "message": "Verify this worktree's AOCI index and configure its host MCP path separately; no host config or runtime state was copied.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect or explicitly create a Kit Git workspace")
    sub = parser.add_subparsers(dest="command", required=True)
    p_status = sub.add_parser("status", help="read-only checkout preflight")
    p_status.add_argument("--repo", required=True, type=Path)
    p_status.add_argument("--mode", required=True, choices=("single", "team"))
    p_status.add_argument("--integration-branch")
    p_create = sub.add_parser("create", help="create one explicitly named Git worktree")
    p_create.add_argument("--repo", required=True, type=Path)
    p_create.add_argument("--target", required=True, type=Path)
    p_create.add_argument("--branch", required=True)
    p_create.add_argument("--base", required=True)
    p_create.add_argument("--integration-branch", required=True)
    args = parser.parse_args()
    try:
        result = (
            status(args.repo, args.mode, args.integration_branch)
            if args.command == "status"
            else create(args.repo, args.target, args.branch, args.base, args.integration_branch)
        )
    except (ValueError, OSError) as exc:
        print(json.dumps({"status": "blocked", "error": str(exc)}, ensure_ascii=True), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
