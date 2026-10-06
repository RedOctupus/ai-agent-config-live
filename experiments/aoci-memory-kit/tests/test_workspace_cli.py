"""RED-first executable workspace admission/creation cases in disposable Git fixtures."""

import json
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "kit-candidate" / "scripts" / "kit-workspace.py"
TEMP_ROOT = ROOT / "artifacts" / "tmp"
assert TEMP_ROOT.resolve().is_relative_to(ROOT.resolve())
TEMP_ROOT.mkdir(parents=True, exist_ok=True)


def git(cwd: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8", check=True)


class WorkspaceCliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=TEMP_ROOT)
        def cleanup():
            assert Path(self.tmp.name).resolve().is_relative_to(TEMP_ROOT.resolve())
            for attempt in range(10):
                try:
                    self.tmp.cleanup()
                    return
                except PermissionError:
                    if attempt == 9:
                        raise
                    time.sleep(0.25)
        self.addCleanup(cleanup)
        self.base = Path(self.tmp.name)
        self.repo = self.base / "repo"
        self.repo.mkdir()
        git(self.repo, "init", "-b", "main")
        (self.repo / "README.md").write_text("fixture\n", encoding="utf-8")
        git(self.repo, "add", "README.md")
        git(self.repo, "-c", "user.name=Kit Test", "-c", "user.email=kit@example.invalid", "commit", "-m", "base")

    def call(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, str(TOOL), *args], capture_output=True, text=True, encoding="utf-8")

    def test_single_clone_is_ready_without_creating_anything(self):
        result = self.call("status", "--repo", str(self.repo), "--mode", "single")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["status"], "ready")
        self.assertEqual(data["checkout_kind"], "clone")
        self.assertFalse(data["creation_required"])

    def test_single_clone_can_use_kit_template_without_aoci_install(self):
        memory = self.repo / "docs" / "memory" / "MEMORY.md"
        memory.parent.mkdir(parents=True)
        template = ROOT / "kit-candidate" / "templates" / "MEMORY.md"
        memory.write_bytes(template.read_bytes())
        state = self.call("status", "--repo", str(self.repo), "--mode", "single")
        self.assertEqual(json.loads(state.stdout)["status"], "ready")
        self.assertIn("AOCI 源码地图：未启用", memory.read_text(encoding="utf-8"))
        self.assertFalse((self.repo / ".aoci").exists())
        self.assertFalse((self.repo / ".codex" / "config.toml").exists())

    def test_team_integration_checkout_needs_workspace(self):
        result = self.call("status", "--repo", str(self.repo), "--mode", "team", "--integration-branch", "main")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["status"], "needs_workspace")
        self.assertTrue(data["creation_required"])
        self.assertEqual(sorted(p.name for p in self.base.iterdir()), ["repo"])

    def test_feature_branch_clone_is_ready(self):
        git(self.repo, "checkout", "-b", "feature/one")
        result = self.call("status", "--repo", str(self.repo), "--mode", "team", "--integration-branch", "main")
        self.assertEqual(json.loads(result.stdout)["status"], "ready")

    def test_explicit_creation_makes_separate_worktree_without_host_config_copy(self):
        config = self.repo / ".codex" / "config.toml"
        config.parent.mkdir()
        config.write_text("[mcp_servers.aoci]\ncommand='local'\n", encoding="utf-8")
        git(self.repo, "status", "--porcelain")  # fixture intentionally has an untracked local host config
        target = self.base / "task-one"
        result = self.call("create", "--repo", str(self.repo), "--target", str(target), "--branch", "task/one", "--base", "HEAD", "--integration-branch", "main")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "created")
        self.assertEqual(git(target, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip(), "task/one")
        self.assertFalse((target / ".codex" / "config.toml").exists())
        state = self.call("status", "--repo", str(target), "--mode", "team", "--integration-branch", "main")
        self.assertEqual(json.loads(state.stdout)["checkout_kind"], "worktree")
        self.assertEqual(json.loads(state.stdout)["status"], "ready")

    def test_create_refuses_dirty_source_and_existing_target(self):
        (self.repo / "README.md").write_text("dirty\n", encoding="utf-8")
        target = self.base / "task-one"
        dirty = self.call("create", "--repo", str(self.repo), "--target", str(target), "--branch", "task/one", "--base", "HEAD", "--integration-branch", "main")
        self.assertNotEqual(dirty.returncode, 0)
        self.assertFalse(target.exists())
        git(self.repo, "checkout", "--", "README.md")
        target.mkdir()
        existing = self.call("create", "--repo", str(self.repo), "--target", str(target), "--branch", "task/one", "--base", "HEAD", "--integration-branch", "main")
        self.assertNotEqual(existing.returncode, 0)


if __name__ == "__main__":
    unittest.main()
