# 需求迭代

> 只追加，不改历史。

| 日期 | 变更 | 原因 | 影响（模块/文档） |
| --- | --- | --- | --- |
| 2026-09-21 | init 项目记忆，并用 README / agent-skills 规则 / memory 导出 / git / hostname 填槽 | 用户要求在本仓 init memory kit 并尽量搜集 | MEMORY / ENVIRONMENT / REQUIREMENTS / FRAMEWORK / FLOW / HANDOVER.md / REFERENCES.md / TODO |
| 2026-09-21 | 目录三分：scaffold / memory / materials；kit 落到 memory/kit/；Hermes 导出落到 memory/hermes/；gitignore 补密钥、取证、_local | 用户要求脚手架、记忆、本地物料分开存放 | README / AGENTS / 脚本路径 / FRAMEWORK / FLOW / HANDOVER / R8 |
| 2026-09-21 | open-code-review 技能补 CI/CD 显式说明与上游 GitHub Actions 指针 | 用户要求 skill 写明可部署到 GitHub Actions | materials/agent-skills/cursor/open-code-review · REFERENCES.md |
| 2026-09-21 | 记忆外移夹 `tests/` 改名为 `annex/`，避免与 pytest / 评测撞名 | 用户确认目录名 annex；TEST-LOG 类型名暂留 | project-memory-kit（cursor+claude）· memory/kit · AGENTS / gitignore |
| 2026-09-21 | annex 日志按内容分前缀：VERIFY / NOTE / CHECKLIST；废弃一律叫 TEST-LOG | 用户要求对照 JinRong 附件实况区分日志种类 | project-memory-kit · memory/kit/annex · AGENTS / mdc |
| 2026-09-21 | **kit v1.1.0**：新增当日索引 `annex/INDEX.md` 与取证忽略片段 `templates/gitignore-memory.txt`；`migration.md` 补「按日期工作日志」四类归位处方；kit 加版本号与升版规则；权威源路径补 `materials/` 前缀 | 诊断 JinRong 分叉：kit 两处缺位——跨任务的当日汇总无载体、按日期日志的收敛处方只够改名（接不住其中约 30% 的坑与结论） | project-memory-kit（cursor+claude）· templates/{annex/INDEX.md,gitignore-memory.txt,MEMORY.md,AGENTS.md,cursor-rule.mdc} · references/{migration.md,design-20260921-dated-log-index.md} · SKILL.md · README.md |
| 2026-09-21 | **kit v1.1.1**：当日索引 init 模板改名为 `annex/_INDEX.md`；版本号同时写 YAML `kit-version` 与正文 `kit v…`；瘦模板、删误拷的无日期 `INDEX.md` 与残留 `templates/tests/` | 用户拍板：init 拷 `_INDEX.md`；JinRong 设计文不动；版本 YAML+正文都写 | project-memory-kit（cursor+claude）· templates/annex/_INDEX.md · SKILL.md · README.md · templates/MEMORY.md · references/migration.md · memory/kit/annex |
