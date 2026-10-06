"""Create a fail-closed, independent Git snapshot of the current SSSS worktree.

Only reads the source. Writes below this experiment directory. No .git, env,
credentials, host config, cache, or symlink/junction is copied.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path, PurePosixPath

SOURCE = Path(r"D:\课程\9.18(工程化落地、就业课准备)\interview_guideline\就业材料\SSSS agent项目")
ROOT = Path(__file__).resolve().parent
DEST = ROOT / "sandbox" / "ssss-agent"
RAW = ROOT / "artifacts" / "raw"
DENY_PARTS = {
    ".git", ".venv", "venv", ".deepeval", ".pytest_cache", "__pycache__",
    "node_modules", ".aoci", "secrets", "credentials", ".codex",
}
DENY_FILES = {".mcp.json", "credentials.json", "id_rsa", "id_ed25519"}
DENY_SUFFIXES = {".pem", ".key", ".p12", ".pfx"}
HOST_CONFIGS = {".claude/settings.json", ".cursor/mcp.json"}


def git(*args: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(SOURCE), *args], check=True, capture_output=True
    ).stdout


def safe_file(rel: str) -> bool:
    p = PurePosixPath(rel)
    if p.is_absolute() or not p.parts or any(part in {"", ".", ".."} for part in p.parts):
        raise ValueError(f"unsafe inventory path: {rel!r}")
    lowered = [part.casefold() for part in p.parts]
    if any(part in DENY_PARTS for part in lowered):
        return False
    name = lowered[-1]
    if name.startswith(".env") and name != ".env.example":
        return False
    if name in DENY_FILES or p.suffix.casefold() in DENY_SUFFIXES:
        return False
    if "/".join(lowered) in HOST_CONFIGS:
        return False
    current = SOURCE
    for part in p.parts:
        current /= part
        if current.is_symlink() or (hasattr(current, "is_junction") and current.is_junction()):
            raise ValueError(f"link/junction refused: {rel!r}")
    if not current.is_file():
        raise ValueError(f"listed path is not a regular file: {rel!r}")
    return True


def inventory() -> tuple[list[dict[str, str | int]], list[str]]:
    names = [b.decode("utf-8") for b in git("ls-files", "-z", "--cached", "--others", "--exclude-standard").split(b"\0") if b]
    if len(names) != len(set(names)):
        raise ValueError("duplicate Git inventory paths")
    selected, denied = [], []
    for rel in sorted(names):
        if not safe_file(rel):
            denied.append(rel)
            continue
        data = (SOURCE / Path(*PurePosixPath(rel).parts)).read_bytes()
        selected.append({"path": rel, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})
    return selected, denied


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("plan", "copy", "verify", "verify-source"))
    args = parser.parse_args()
    if SOURCE.resolve() == DEST.resolve() or SOURCE in DEST.parents:
        raise SystemExit("source/destination overlap")
    if args.mode in ("verify", "verify-source"):
        planned = json.loads((RAW / "snapshot-inventory.json").read_text(encoding="utf-8"))
        current, denied = inventory()
        if current != planned["selected"] or denied != planned["denied"]:
            raise SystemExit("source inventory or content changed since preflight")
        if git("status", "--porcelain=v1", "-z", "-uall").hex() != planned["source_status_hex"]:
            raise SystemExit("source Git status changed since preflight")
        if args.mode == "verify" and DEST.exists():
            for item in current:
                rel = str(item["path"])
                copy = DEST / Path(*PurePosixPath(rel).parts)
                if not copy.is_file() or hashlib.sha256(copy.read_bytes()).hexdigest() != item["sha256"]:
                    raise SystemExit(f"sandbox snapshot mismatch: {rel}")
        print(f"PASS: source unchanged; {len(current)} selected files match preflight" +
              (" and sandbox copy" if args.mode == "verify" else ""))
        return

    selected, denied = inventory()
    report = {
        "source": str(SOURCE), "destination": str(DEST),
        "source_head": git("rev-parse", "HEAD").decode().strip(),
        "source_status_hex": git("status", "--porcelain=v1", "-z", "-uall").hex(),
        "selected": selected, "denied": denied,
    }
    if args.mode == "plan":
        if DEST.exists():
            raise SystemExit("destination already exists; never overwrite a sandbox")
        write_json(RAW / "snapshot-inventory.json", report)
        print(f"PLAN: {len(selected)} files, {sum(int(x['bytes']) for x in selected)} bytes; denied {len(denied)}")
        print(f"Manifest: {RAW / 'snapshot-inventory.json'}")
        print("Denied paths:", denied)
        return
    planned = json.loads((RAW / "snapshot-inventory.json").read_text(encoding="utf-8"))
    if report != planned:
        raise SystemExit("source changed since plan; rerun plan and review")
    if DEST.exists():
        raise SystemExit("destination already exists; never overwrite a sandbox")
    DEST.mkdir(parents=True)
    for item in selected:
        rel = str(item["path"])
        src = SOURCE / Path(*PurePosixPath(rel).parts)
        dst = DEST / Path(*PurePosixPath(rel).parts)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst, follow_symlinks=False)
        if hashlib.sha256(dst.read_bytes()).hexdigest() != item["sha256"]:
            raise SystemExit(f"copy mismatch: {rel}")
    subprocess.run(["git", "init", "--quiet", str(DEST)], check=True)
    subprocess.run(["git", "-C", str(DEST), "add", "--all"], check=True)
    subprocess.run([
        "git", "-C", str(DEST), "-c", "user.name=AOCI Sandbox",
        "-c", "user.email=sandbox@example.invalid", "commit", "--quiet",
        "-m", "Isolated SSSS worktree snapshot",
    ], check=True)
    print(f"COPIED: {len(selected)} files into independent Git sandbox {DEST}")


if __name__ == "__main__":
    main()
