"""End-state assertions for the SSSS sandbox Kit→AOCI code-change exercise."""

import hashlib
import importlib.util
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT / "sandbox" / "ssss-agent"
SOURCE = REPO / "ssss_agent" / "services" / "review_contract.py"
MEMORY = REPO / "docs" / "memory" / "MEMORY.md"
VERIFY = REPO / "docs" / "memory" / "annex" / "VERIFY-20261006-kit-aoci-source-task.md"
ITERATION = REPO / "docs" / "memory" / "ITERATION.md"
BIN = ROOT / "artifacts" / "bin" / "aoci.exe"


class SandboxFlowTests(unittest.TestCase):
    def test_memory_enables_aoci_by_one_pointer(self):
        text = MEMORY.read_text(encoding="utf-8")
        self.assertEqual(text.count("<!-- kit:aoci-status -->"), 1)
        line = next(line for line in text.splitlines() if "AOCI 源码地图：已启用" in line)
        self.assertIn("../../AGENTS.md", line)
        self.assertIn("Kit VERIFY/ITERATION", line)
        self.assertTrue((MEMORY.parent / "../../AGENTS.md").resolve().is_file())

    def test_source_has_equivalent_finite_check_and_changed_hash(self):
        text = SOURCE.read_text(encoding="utf-8")
        self.assertIn("if not math.isfinite(number):", text)
        self.assertNotIn("math.isnan(number) or math.isinf(number)", text)
        inventory = json.loads((ROOT / "artifacts" / "raw" / "snapshot-inventory.json").read_text(encoding="utf-8"))
        before = next(row["sha256"] for row in inventory["selected"] if row["path"] == "ssss_agent/services/review_contract.py")
        self.assertNotEqual(hashlib.sha256(SOURCE.read_bytes()).hexdigest(), before)

    def test_finite_check_preserves_existing_decisions(self):
        spec = importlib.util.spec_from_file_location("sandbox_review_contract", SOURCE)
        module = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(module)
        cases = (
            (0, True), (0.5, True), (1, True), (-0.1, False), (1.1, False),
            (float("nan"), False), (float("inf"), False), (-float("inf"), False),
            ("0.2", True), ("bad", False), (None, False), (True, True), (False, True),
        )
        for value, expected in cases:
            with self.subTest(value=value):
                self.assertEqual(module._confidence_ok(value), expected)

    def test_aoci_final_index_is_aligned_to_changed_source(self):
        result = subprocess.run([str(BIN), "--repo", str(REPO), "verify", "--json"], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stderr[:1000])
        state = json.loads(result.stdout)["governance"]
        self.assertTrue(state["governance_aligned"])
        self.assertEqual(state["code_drift"]["stale"], [])

    def test_kit_closeout_is_written_in_same_sandbox(self):
        report = VERIFY.read_text(encoding="utf-8")
        self.assertIn("review_contract.py", report)
        self.assertIn("AOCI", report)
        self.assertIn("verify", report)
        self.assertIn("Kit×AOCI联动沙盒", ITERATION.read_text(encoding="utf-8"))

    def test_original_ssss_stays_untouched(self):
        result = subprocess.run(["python", str(ROOT / "snapshot.py"), "verify-source"], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
