"""Executable W07: conflicting source branches never silently merge AOCI text."""

import subprocess
import tempfile
import time
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMP_ROOT = ROOT / "artifacts" / "tmp"
TEMP_ROOT.mkdir(parents=True, exist_ok=True)


def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True,
        text=True, encoding="utf-8", errors="replace",
    )
    if check and result.returncode:
        raise AssertionError(result.stderr)
    return result


class SourceConflictTests(unittest.TestCase):
    def test_same_object_conflict_requires_human_without_map_merge(self):
        tmp = tempfile.TemporaryDirectory(dir=TEMP_ROOT)
        try:
            repo = Path(tmp.name)
            git(repo, "init", "-b", "main")
            source = repo / "service.py"
            source.write_text("def value():\n    return 'base'\n", encoding="utf-8")
            map_file = repo / "aoci.code.txt"
            map_file.write_text("service.py[DB5T]: F:base | R:- | A:value | S:-\n", encoding="utf-8")
            git(repo, "add", "service.py", "aoci.code.txt")
            git(repo, "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "base")

            for branch, value in (("task/a", "alpha"), ("task/b", "beta")):
                git(repo, "checkout", "-b", branch, "main")
                source.write_text(f"def value():\n    return '{value}'\n", encoding="utf-8")
                map_file.write_text(f"service.py[DB5T]: F:{value} | R:- | A:value | S:-\n", encoding="utf-8")
                git(repo, "add", "service.py", "aoci.code.txt")
                git(repo, "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", value)

            git(repo, "checkout", "main")
            # Integrate *source only*, leaving the formal map untouched until a fresh pass.
            git(repo, "restore", "--source", "task/a", "--", "service.py")
            git(repo, "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-am", "integrate alpha source")
            patch = git(repo, "diff", "main~1", "task/b", "--", "service.py").stdout
            applied = subprocess.run(["git", "-C", str(repo), "apply", "-"], input=patch,
                                     capture_output=True, text=True, encoding="utf-8")
            self.assertNotEqual(applied.returncode, 0, "conflicting source must stop for human resolution")
            self.assertEqual(map_file.read_text(encoding="utf-8"), "service.py[DB5T]: F:base | R:- | A:value | S:-\n")
            self.assertEqual(source.read_text(encoding="utf-8"), "def value():\n    return 'alpha'\n")
        finally:
            target = Path(tmp.name).resolve()
            self.assertTrue(target.is_relative_to(TEMP_ROOT.resolve()))
            for attempt in range(10):
                try:
                    tmp.cleanup()
                    break
                except PermissionError:
                    if attempt == 9:
                        raise
                    time.sleep(0.25)


if __name__ == "__main__":
    unittest.main()
