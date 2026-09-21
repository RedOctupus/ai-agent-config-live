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
| 2026-09-21 | **更正上一行**：`kit v1.1.1` 的版本号按升版规则应为 **`v1.2.0`**——把 init 拷贝目标从 `INDEX.md` 改成 `_INDEX.md`，属「改维护口令」，应中位 +1。已改 `SKILL.md` 的 `kit-version` / 正文 / 升版示例、`README.md` 版本行、`templates/MEMORY.md` §5、设计文 §3.4 加落地戳；**上一行保留不改** | ① 误标末位会让项目读成「补丁，不用跟版」，从而漏掉一次真的拷贝目标变更；② 我最初误将上一行**整行替换**，违反本文件「只追加，不改历史」，现恢复原行并追加本行 | project-memory-kit（cursor+claude）· SKILL.md · README.md · templates/MEMORY.md · references/design-20260921-dated-log-index.md · memory/kit |
| 2026-09-21 | **kit v1.2.1**：`templates/MEMORY.md` §5 的 HANDOVER 行补上「与顶部『最后核实』」（原文只提「该条核实日期」，漏了文件顶部的核实点）；连带刷新 `SKILL.md` 版本号与升版示例、`README.md` 版本行、`templates/MEMORY.md` §5 版本行、设计文进度戳、并把「补句 vs 改口令」判据补进升版规则 | 审查本仓 §0 HEAD 漏刷时全库 grep 发现：一个项目记 HEAD 恰两处（MEMORY §0 与 HANDOVER 顶部），而**日常真正被读的 §5 表只要求刷其中一处的兄弟字段**，照它干活的 Agent 会规律性漏刷顶部「最后核实」 | project-memory-kit（cursor+claude）· templates/MEMORY.md · SKILL.md · README.md · references/design-20260921-dated-log-index.md · memory/kit |
| 2026-09-21 | **kit v1.3.0**：MEMORY §0「工作分支」只留分支名；短哈希只写 HANDOVER 顶部「最后核实」。常驻口令去掉「刷新 §0 HEAD」 | 两处都记短哈希会把两种时钟误当成漏刷；用户选结构收敛（一处事实一处写） | project-memory-kit（cursor+claude）· templates/{MEMORY.md,HANDOVER.md,AGENTS.md,cursor-rule.mdc} · SKILL.md · README.md · references/{migration.md,design-20260921-dated-log-index.md} · memory/kit · AGENTS.md · `.cursor/rules/project-memory.mdc` |
