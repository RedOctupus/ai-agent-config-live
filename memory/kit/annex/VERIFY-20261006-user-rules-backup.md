# VERIFY：Cursor 用户规则全文备份

- 日期：2026-10-06
- 关联：账号云端 User Rules 不在 Git 里
- 风险等级：LOW

## 改了什么

- 文件：`.cursor/rules/user-rules.mdc`（alwaysApply）、`AGENTS.md`、`memory/kit/MEMORY.md` §3、`ITERATION.md`、`annex/INDEX-20261006.md`
- 行为变化：本仓 Cursor 会话会再注入一份与当前 User Rules 一致的全文。不读 mdc 的 Agent 从 `AGENTS.md` 转到该文件

## 已执行

| 类型 | 命令或步骤 | 结果 |
| --- | --- | --- |
| 对照 | 与本会话注入的 User Rules 逐条核对 | 提交协议、PR、网页验收、表述、冲突裁决、规则 1–5、技能、简体中文都在 |
| 体量 | `python scaffold/scripts/check-memory-size.py memory/kit/MEMORY.md` | PASS：全文 217 行，§0 实义 7 行、624 字符，最长行 179 |

## 未执行

- 项：改 Cursor Settings 里的账号云端 User Rules
- 原因：那份在账号侧，本仓文件是备份和本仓常驻副本，不能从这里回写设置页

## 结论

- 需求是否覆盖：全文在本仓负责的常驻规则文件里，指针在 AGENTS 和 MEMORY
- 旧功能是否破坏：未改 project-memory 规则正文
- 剩余风险：以后只改账号规则或只改本仓文件，两处会漂移
