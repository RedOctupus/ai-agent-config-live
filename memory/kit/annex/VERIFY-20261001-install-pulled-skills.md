# VERIFY：把已拉取的 kit / 新技能装到本机运行时

- 日期：2026-10-01
- 关联 TODO：无（用户口头：更新和装一下）
- 风险等级：LOW

## 改了什么

- 本机安装目录（由仓库副本拷入，排除 `_sandbox`）：
  - Cursor / Claude / Codex：`project-memory-kit` 升到 **v1.6.0**（各 30 个文件）
  - Cursor / Codex：新增 `deepeval`（16）、`hindsight-agent-memory`（14）
  - Cursor / Claude / Codex：新增 portable `agent-memory-design`（12）
- 未改仓库技能正文；未动 Cursor 内置 `skills-cursor`、插件缓存、Codex 原有技能目录。
- Codex 继续跟 Cursor 个人库对齐：上述 4 个目录与 Cursor 现场逐字一致。Cursor 个人技能由 22 个变为 **25** 个。

## 已执行

| 类型 | 命令或步骤 | 结果 |
| --- | --- | --- |
| 手工 | `robocopy /MIR /XD _sandbox` 共 10 对目录 | PASS：退出码均 < 8 |
| 手工 | Python `filecmp` 仓库→Cursor/Claude，再 Cursor→Codex | PASS：30+30+16+14+12+12+30+16+14+12，无只在一侧 / 无内容差 |
| 手工 | 读三处 `project-memory-kit/SKILL.md` 的 `kit-version` | PASS：均为 `1.6.0` |
| 手工 | `python scaffold/scripts/check-memory-size.py memory/kit/MEMORY.md` | PASS：体量达标 |

## 未执行

- 项：新开 Cursor / Claude Code / Codex 会话，确认技能名出现在可用列表
- 原因：安装约定是下一轮加载才生效；本轮只验文件落盘
- 项：跑 `deepeval` / `agent-memory-design` 评测或业务路径
- 原因：未授权装外部依赖；未当业务流程已通

## 结论

- 需求是否覆盖：用户要求「更新和装」已覆盖上一轮点名的 kit 与三套新技能；Codex 仍与 Cursor 个人库同名目录一致。
- 旧功能是否破坏：未覆盖其它已装技能；Codex 原有 16 个非 Cursor 目录仍在。
- 剩余风险：`materials/agent-skills/README.md` 的 cursor 平铺清单未写 `hindsight-agent-memory`，仓内有目录且已按用户口头安装。
- 建议人工再验：新开三个运行时窗口，看能否点到这四个技能名。
