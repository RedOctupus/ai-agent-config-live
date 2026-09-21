# 服务对象大环境（现状 / As-Is）

> 描述**你要服务的对象所处的大环境**：对方是谁、现在怎么办事、角色和对象是什么。
> 不是本项目要做成什么样（那是需求讨论），也不是系统内部怎么流转（那是 FLOW）。
> 不写函数实现；不写技术选型。
> 2026-09-21 根据 README、`materials/agent-skills/README.md`、`memory/hermes/*.md`、本机 `hostname` 归纳；未跟完项目史，可能不全。

------

## 1. 服务对象与角色（现在）

```text
服务谁：机主本人（GitHub RedOctupus；档案见 memory/hermes/user-profile.md）
谁在办事：机主在 Cursor / Hermes / Claude Code / Codex 里改技能、配 Agent
谁审批：无第二人审批；双机以台式机为准（冲突拿不准时）
谁使用结果：机主自己；换机或重装后从本私仓恢复
```

## 2. 对方现在怎么办事

```text
日常在 Cursor 或 Hermes 里装/改个人技能，有变化才拷进本仓 materials/ 对应目录并 push。
Hermes 技能树在 materials/skills/（分类 + manifest）；Cursor/Claude/可移植技能在 materials/agent-skills/。
本机技能目录是权威工作副本；远端是备份。明确禁止「clone 完自动覆盖本机已装技能」。
两台 Windows：家里台式机 SC-202601081030、学校笔记本 DESKTOP-DKO2LI9（本次所在机）。
灾难恢复按 README：clone → scaffold/scripts/restore.sh → 填 ~/.hermes/.env → hermes doctor。
本仓交接读 memory/kit/；Hermes 导出读 memory/hermes/。
另有 Uniflo 等其它项目，不在本仓范围内。
```

## 3. 主路径（现状逐步）

1. 在某一 Agent 运行时里改技能或配置（本机 `~/.cursor/skills` 或 `~/.hermes/skills` 等）
2. 按运行时拷到本仓 `materials/agent-skills/cursor|claude|portable/` 或 `materials/skills/<category>/`
3. git commit / push 到 GitHub 私仓 `RedOctupus/ai-agent-config-live`
4. 换机或重装时 clone，按 README Quick Recovery 恢复，再手工填密钥

## 4. 环境里的关键对象

| 名称 | 含义 | 关键字段 / 单据 |
| --- | --- | --- |
| 个人技能目录 | 某运行时当前生效的 SKILL.md 树 | 目录名 = skill name |
| 本仓备份夹 | 按运行时分夹的副本 | `materials/agent-skills/` · `materials/skills/` |
| Hermes 记忆导出 | `memory/hermes/`，与 kit 的 `memory/kit/` 不是同一套 | user-profile / environment / machine |
| Superpowers 插件缓存 | Cursor 插件技能，备份在 `materials/agent-skills/cursor/plugins/superpowers/` | 来自 `~/.cursor/plugins/cache/...` |

## 5. 痛点与约束（环境里已有的）

```text
双机技能会分叉；约定冲突偏台式机，避免笔记本覆盖桌面较新稿。
catalog / README Last sync 停在 2026-05-24，现场工具版本可能已变。
密钥必须留在本机 ~/.hermes/.env，仓内只有 .env.template。
Cursor 内置 skills-cursor 明确不备份。
```
