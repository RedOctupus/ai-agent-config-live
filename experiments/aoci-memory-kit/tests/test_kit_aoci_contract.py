"""Executable contract for the isolated Kit×AOCI candidate, not production Kit files."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "kit-candidate"


def read(rel: str) -> str:
    return (CANDIDATE / rel).read_text(encoding="utf-8")


class KitAociContractTests(unittest.TestCase):
    def test_init_keeps_mode_and_aoci_independent_without_forcing_single_user(self):
        init = read("SKILL.md").split("## Init", 1)[1].split("## 日常维护", 1)[0]
        self.assertIn("单人 / 多人", init)
        self.assertIn("AOCI 源码地图：启用 / 不启用", init)
        self.assertIn("两个独立选择", init)
        self.assertIn("单人 clone 本身就是可用工作区", init)
        self.assertIn("单人模式默认不强制选择", init)

    def test_unselected_project_explicitly_says_aoci_off(self):
        memory = read("templates/MEMORY.md")
        self.assertIn("<!-- kit:aoci-status -->", memory)
        self.assertIn("AOCI 源码地图：未启用", memory)
        self.assertIn("直接核对源码和测试", memory)

    def test_team_root_owns_repository_aoci_status(self):
        root = read("templates/ROOT-MEMORY.md")
        self.assertIn("<!-- kit:aoci-status -->", root)
        self.assertIn("AOCI 源码地图：未启用", root)
        self.assertIn("模块 MEMORY 只指向根状态", root)
        self.assertIn("架构负责人", root)

    def test_team_init_replaces_module_default_status_with_root_pointer(self):
        init = read("SKILL.md").split("## Init", 1)[1].split("## 日常维护", 1)[0]
        self.assertIn("将模块 MEMORY 的默认 AOCI 状态行替换为指向根 ROOT-MEMORY.md 的指针", init)
        self.assertIn("模块不得保留单人模板的“未启用”结论", init)

    def test_opt_out_never_installs_aoci(self):
        init = read("SKILL.md").split("## Init", 1)[1].split("## 日常维护", 1)[0]
        self.assertIn("用户选择不启用", init)
        self.assertIn("不得运行 aoci init", init)
        self.assertIn("不配置项目级 MCP", init)

    def test_enabled_source_change_joins_kit_closeout(self):
        skill = read("SKILL.md")
        self.assertIn("仅启用 AOCI 的源码任务", skill)
        self.assertIn("aoci_rules", skill)
        self.assertIn("aoci_overview", skill)
        self.assertIn("delivery_receipt_version", skill)
        self.assertIn("aoci_maintain", skill)
        self.assertIn("verify → check → Guide", skill)
        self.assertIn("Kit VERIFY/ITERATION", skill)
        self.assertIn("不得宣称代码交付闭环完成", skill)

    def test_deployment_is_one_skill_plus_one_project_mcp(self):
        deployment = (ROOT / "DEPLOYMENT.md").read_text(encoding="utf-8")
        self.assertIn("Kit 是 Skill，不是 MCP", deployment)
        self.assertIn("AOCI 是项目级 stdio MCP", deployment)
        self.assertIn("每台机器", deployment)
        self.assertIn("绝对路径", deployment)
        self.assertIn("Cursor", deployment)

    def test_candidate_version_matches_new_project_template(self):
        skill = read("SKILL.md")
        memory = read("templates/MEMORY.md")
        self.assertIn('kit-version: "1.7.1"', skill)
        self.assertIn("本记忆按 kit v1.7.1 建立", memory)


if __name__ == "__main__":
    unittest.main()
