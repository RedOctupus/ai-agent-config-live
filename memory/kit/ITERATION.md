# 需求迭代

> 只追加，不改历史。

| 日期 | 变更 | 原因 | 影响（模块/文档） |
| --- | --- | --- | --- |
| 2026-09-21 | init 项目记忆，并用 README / agent-skills 规则 / memory 导出 / git / hostname 填槽 | 用户要求在本仓 init memory kit 并尽量搜集 | MEMORY / ENVIRONMENT / REQUIREMENTS / FRAMEWORK / FLOW / HANDOVER.md / REFERENCES.md / TODO |
| 2026-09-21 | 目录三分：scaffold / memory / materials；kit 落到 memory/kit/；Hermes 导出落到 memory/hermes/；gitignore 补密钥、取证、_local | 用户要求脚手架、记忆、本地物料分开存放 | README / AGENTS / 脚本路径 / FRAMEWORK / FLOW / HANDOVER / R8 |
| 2026-09-21 | open-code-review 技能补 CI/CD 显式说明与上游 GitHub Actions 指针 | 用户要求 skill 写明可部署到 GitHub Actions | materials/agent-skills/cursor/open-code-review · REFERENCES.md |
| 2026-09-21 | 记忆外移夹 `tests/` 改名为 `annex/`，避免与 pytest / 评测撞名 | 用户确认目录名 annex；TEST-LOG 类型名暂留 | project-memory-kit（cursor+claude）· memory/kit · AGENTS / gitignore |
| 2026-09-21 | annex 日志按内容分前缀：VERIFY / NOTE / CHECKLIST；废弃一律叫 TEST-LOG | 用户要求对照 JinRong 附件实况区分日志种类 | project-memory-kit · memory/kit/annex · AGENTS / mdc |
