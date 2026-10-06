"""RED-first Kit contract for optional single mode and isolated team workspaces."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "kit-candidate"


def read(path: str) -> str:
    return (KIT / path).read_text(encoding="utf-8")


class WorkspaceContractTests(unittest.TestCase):
    def test_authoritative_claude_and_cursor_skills_match_candidate(self):
        repo = ROOT.parents[1]
        claude = repo / "materials" / "agent-skills" / "claude" / "project-memory-kit"
        cursor = repo / "materials" / "agent-skills" / "cursor" / "project-memory-kit"
        for rel in (
            "SKILL.md", "templates/AGENTS.md", "templates/cursor-rule.mdc",
            "templates/ROOT-MEMORY.md", "templates/MEMORY.md",
            "scripts/kit-workspace.py",
        ):
            with self.subTest(path=rel):
                expected = (KIT / rel).read_bytes()
                self.assertEqual((claude / rel).read_bytes(), expected)
                self.assertEqual((cursor / rel).read_bytes(), expected)
        self.assertEqual((claude / "README.md").read_bytes(), (cursor / "README.md").read_bytes())

    def test_human_readme_explains_optional_deployment(self):
        repo = ROOT.parents[1]
        readme = (repo / "materials" / "agent-skills" / "claude" / "project-memory-kit" / "README.md").read_text(encoding="utf-8")
        self.assertIn("scripts/kit-workspace.py", readme)
        self.assertIn("AOCI 默认不启用", readme)
        self.assertIn("单人 clone", readme)
        self.assertIn("源码先于全局图", readme)

    def test_human_readme_has_version_neutral_aoci_upgrade_gate(self):
        repo = ROOT.parents[1]
        readme = (repo / "materials" / "agent-skills" / "claude" / "project-memory-kit" / "README.md").read_text(encoding="utf-8")
        section = readme.split("## AOCI 升级清单", 1)[1].split("\n## ", 1)[0]
        for required in (
            "目标版本", "用户确认", "未完成事务", "旧二进制", "SHA-256",
            "工作区", "宿主实际运行版本", "--repo", "Verify", "Check", "Guide",
            "回滚", "不重建索引", "不自动覆盖", "Kit 版本不必跟着升级",
            "docs/upgrading.md", "docs/install.md", "docs/rollback.md",
        ):
            with self.subTest(required=required):
                self.assertIn(required, section)
        self.assertNotIn("v0.1.0-rc18", section, "upgrade checklist must not freeze a future version")

    def test_single_clone_is_a_workspace_without_choice_or_worktree(self):
        skill = read("SKILL.md")
        self.assertIn("单人 clone 本身就是可用工作区", skill)
        self.assertIn("不强制创建 worktree", skill)
        self.assertIn("AOCI 仍须用户明确启用", skill)

    def test_team_workspace_is_not_person_or_module(self):
        skill = read("SKILL.md")
        self.assertIn("工作区不等于人员或模块", skill)
        self.assertIn("独立 clone 或 Git worktree", skill)
        self.assertIn("不能从 Git 状态证明没有其他 Agent 同时写该目录", skill)

    def test_newcomer_entry_warns_before_team_source_write(self):
        for path in ("templates/AGENTS.md", "templates/cursor-rule.mdc"):
            with self.subTest(path=path):
                text = read(path)
                self.assertIn("kit-workspace.py status", text)
                self.assertIn("集成分支", text)
                self.assertIn("不得静默创建", text)
        root = read("templates/ROOT-MEMORY.md")
        self.assertIn("**集成分支：**", root)
        self.assertIn("工作区准入", root)

    def test_personal_index_is_proposal_not_merge_input(self):
        skill = read("SKILL.md")
        self.assertIn("个人 AOCI 地图只作为集成提案", skill)
        self.assertIn("先合并源码，再对合并后的源码重新签发", skill)
        self.assertIn("不得文本合并个人 aoci.code.txt", skill)
        self.assertIn("同一对象冲突", skill)
        self.assertIn("人工裁决", skill)

    def test_aoci_is_optional_and_version_decoupled(self):
        skill = read("SKILL.md")
        self.assertIn("Kit 不内嵌 AOCI 版本和状态机", skill)
        self.assertIn("AOCI 不可用不等于未启用", skill)
        self.assertIn("不得自动升级 AOCI", skill)
        self.assertIn("不得自动覆盖宿主配置", skill)

    def test_workspace_helper_is_shipped_by_init(self):
        skill = read("SKILL.md")
        self.assertIn("scripts/kit-workspace.py", skill)
        self.assertTrue((KIT / "scripts" / "kit-workspace.py").is_file())


if __name__ == "__main__":
    unittest.main()
