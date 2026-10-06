# VERIFY：Cursor 用户全局规则改为可借鉴资产

- 日期：2026-10-06
- 关联：账号云端 User Rules 不在 Git 里
- 风险等级：LOW

## 改了什么

- 文件：新增 `materials/cursor-user-rules/README.md` 与 `RULES.md`；删除 `.cursor/rules/user-rules.mdc`；`AGENTS.md` 去掉「先读并遵守」；`MEMORY.md` §3/§4、`FRAMEWORK.md`、`HANDOVER.md`、`README.md` 结构树、`ITERATION.md`、`annex/INDEX-20261006.md` 改为指向物料目录
- 行为变化：本仓 Cursor 会话不再多注入一份 User Rules。其他 Agent 从 `materials/cursor-user-rules/` 读快照来借鉴；人类点名后才抄进目标项目或账号

## 已执行

| 类型 | 命令或步骤 | 结果 |
| --- | --- | --- |
| 对照 | `RULES.md` 与先前会话里的 User Rules 逐条核对 | 提交、拉取请求、网页验收、表述、冲突裁决、规则 1–5、技能、简体中文都在 |
| 注入 | 确认 `.cursor/rules/` 只剩 `project-memory.mdc` | 见本次删除后的目录 |
| 体量 | `python scaffold/scripts/check-memory-size.py memory/kit/MEMORY.md` | PASS：全文 217 行，§0 实义 7 行、624 字符，最长行 179 |

## 未执行

- 项：改 Cursor Settings 里的账号 User Rules
- 原因：账号规则仍是活的那一份；本目录只保存可借鉴快照，不回写设置页

## 结论

- 需求是否覆盖：全文在物料层，附带借鉴步骤和维护约定；本仓常驻规则未被这份快照替换
- 旧功能是否破坏：`project-memory.mdc` 未改
- 剩余风险：账号规则以后变了，要人点名才更新 `RULES.md`，两边不会自动对齐
