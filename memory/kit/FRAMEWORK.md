# 项目框架

> 「已定」只收录仓库 README / agent-skills 规则里机主已经写明的约定，以及目录里已经存在的形态。不是一次新的【框架讨论】。未写进那些文件的运行时/库一律放「待商量」。

------

## 1. 技术选型

| 技术栈（解决什么） | 已定（用户已同意） | 待商量 |
| --- | --- | --- |
| 备份载体 | Git + GitHub 私仓 `RedOctupus/ai-agent-config-live` |  |
| 技能文档格式 | 各技能目录内 `SKILL.md`（及可选 scripts/templates） |  |
| Cursor 技能落点 | 仓库 `materials/agent-skills/cursor/` ← 本机 `~/.cursor/skills`（只推） | 本仓是否再建 `.cursor/skills/` 项目技能（当前没有） |
| Claude 技能落点 | 仓库 `materials/agent-skills/claude/` |  |
| 可移植技能 | `materials/agent-skills/portable/` |  |
| Hermes 技能落点 | 仓库 `materials/skills/<category>/` |  |
| 同步/恢复 | `scaffold/scripts/` 下 sync-skills / sync-memory / restore / auto-sync | 是否在笔记本改用 PowerShell 等价脚本（现有为 sh） |
| 本仓目录分层 | `scaffold/` 脚手架；`memory/` 记忆；`materials/` 本地物料 |  |
| 应用运行时 | 无（本仓不是服务） | 不要默认加 Docker / DB / Web 框架 |

```text
不用什么：不把本仓做成可部署应用；不备份 Cursor 内置技能
关键取舍（用户已认可）：远端是备份不是本机权威；冲突偏台式机；三层目录分开存放
```

## 2. 能力模块

| 模块 | 职责 | 依赖谁 |
| --- | --- | --- |
| `scaffold/scripts/` | 同步、灾难恢复、kit 体量门闸 | git / 本机路径 |
| `memory/kit/` | 本仓 project-memory-kit 交接 | kit 模板（其它项目默认仍是 docs/memory/） |
| `memory/hermes/` | Hermes 长期记忆导出 | `~/.hermes/memories/` |
| `materials/hermes/` | 脱敏后的 Hermes 配置与 env 模板 | 本机 `~/.hermes/` |
| `materials/skills/` | Hermes 技能全量备份 + `manifest.md` | Hermes skills 目录 |
| `materials/agent-skills/` | 按运行时分类的个人技能备份 | Cursor / Claude / 可移植约定 |
| `business-context-first-agent-design` | 业务域 → 生命周期 → 角色任务 → 上下文 → Agent → 原子能力 → 能力模块 → 角色视图 → 跨域回流的设计门闸 | `project-memory-kit` 路由 + 可选 `BUSINESS-CONTEXT.md` 模板 |
| `materials/tools/` | 本机 CLI/Agent 工具清单 | 人工维护 catalog |
| `materials/plans/` | 历史计划 | 无运行时依赖 |
| `materials/_local/` | 本机临时物料（不入库） | `.gitignore` |

## 3. 分层约定

```text
允许：只增备份文件、记忆文档、清单；改技能正文时同步对应备份夹

禁止：
- Agent 未经明示把远端技能安装到本机
- 把密钥写入仓内任何文件
- 把 memory/hermes/ 与 memory/kit/ 混成一份
```

## 4. 骨架一句话（与 MEMORY 第 2 节「项目框架」同一句）

```text
无应用运行时；三层目录 + Markdown 技能树 + shell 同步脚本 + GitHub 私仓。
```
