# 项目记忆（人 + Agent 共用）

> 各阶段的**简化快照**（门闸索引）。只留基础信息，不写源文件正文。
> 需要澄清时打开对应源文件。Agent 改代码前必须能回答文末「阅读完成门闸」。

------

## 0. 交接清单

- **项目是什么：** 私人备份 Hermes / Cursor / Claude 技能与本机工具清单，并作为 project-memory-kit 权威仓。
- **当前进度：** 目录已三分：`scaffold/`、`memory/{kit,hermes}/`、`materials/`。README Last sync **2026-05-24** 可能过期。
- **端到端 / 交付记录：** [INDEX-20260921](annex/INDEX-20260921.md) · 最近 [kit-v1.3.1](annex/VERIFY-20260921-kit-v1.3.1.md)
- **必知事实：** 见 [HANDOVER](HANDOVER.md)（仅供参考，行动前先核实）
- **外部：** 见 [REFERENCES](REFERENCES.md)；计划见 [plans/2026-05-24_192600-agent-config-repo.md](../../materials/plans/2026-05-24_192600-agent-config-repo.md)
- **工作分支：** `main`

------

## 1. 项目简介

- **名称：** ai-agent-config-live
- **当前阶段：** Maintenance
- **当前优先级：** 稳定性（备份正确、禁止远端技能自动覆盖本机）

------

## 2. 阶段快照

| 阶段 | 当前一句话 | 源文件 |
| --- | --- | --- |
| 服务对象大环境 | 机主在两台 Windows 上用 Hermes/Cursor/Claude 维护个人 Agent 技能，本仓是单向远程备份。 | `ENVIRONMENT.md` |
| 需求目的 | 技能与配置能从 GitHub 私仓恢复，且 Cursor 技能只推不自动拉。 | `REQUIREMENTS.md` |
| 项目框架 | 无应用运行时；三层目录 + Markdown 技能树 + shell 同步脚本 + GitHub 私仓。 | `FRAMEWORK.md` |
| 实现流程 | 本机改技能 → 拷进 `materials/` 对应夹 → commit/push；灾难恢复走 `restore.sh`。 | `FLOW.md` |

------

## 3. 约束

**硬阀门：技术选型（框架讨论）**

框架确立**基于各技术栈的选择**：库、中间件、语言/框架、存储、向量库、解析器、第三方服务等，**每一项**都须先与用户商量并获明确同意，才能写入 `FRAMEWORK.md`、改 MEMORY 框架快照、或据此编码 / 进 Plan。禁止自行拍板、拿常见方案当已定、把「建议」写成「用什么」、未确认就新增依赖——未确认项只能放「待商量」，不能当框架已立。

**禁止触碰：**

```text
materials/hermes/.env 及任何 API key / token 正文
把仓库技能静默拷回 ~/.cursor/skills 或替本机注册/启用技能
~/.cursor/skills-cursor（Cursor 内置，不备份、不改）
```

**高风险（改前需确认）：** 覆盖本机已装技能、改同步方向、删 `materials/skills/` 或 `materials/agent-skills/` 大目录、改 GitHub 私仓可见性。

**开发开关：**

| 项 | YES / NO |
| --- | --- |
| 允许新增依赖 | NO（本仓不是应用；加运行时依赖须先问） |
| 允许重构 | NO（默认只备份/文档；目录搬家须先问） |
| 允许改表 / schema | NO（无业务库） |
| 允许改接口协议 | NO（无对外 API） |

**已拍板（跨线规则 · 一行一条，只留结论）：**

```text
Cursor 技能只往远程更新：~/.cursor/skills → materials/agent-skills/cursor/，有变化才提交推送
不自动拉本机、不自动注册（除非用户明确说从远端拉某个技能下来用）
双机合并上传：台式机 SC-202601081030 与笔记本 DESKTOP-DKO2LI9；冲突取较新，拿不准偏台式机
不含 Cursor 内置 skills-cursor；Superpowers 插件技能备份 ≠ 自动重装插件
project-memory-kit 权威源是本仓 materials/agent-skills/ 下 cursor 与 claude 两份副本，须保持一致
```

**特殊规则：**

```text
memory/hermes/ 是 Hermes 长期记忆导出；memory/kit/ 是本仓 project-memory-kit；其它项目 kit 默认仍是 docs/memory/
本会话机器是 DESKTOP-DKO2LI9（学校笔记本）；materials/tools/catalog.md 版本号可能过期
```

------

## 4. 入口与运行

```text
关键文件：README.md ； materials/agent-skills/README.md ； materials/skills/manifest.md
如何启动：本仓无常驻服务。恢复走 ./scaffold/scripts/restore.sh ；技能备份走 ./scaffold/scripts/sync-skills.sh
配置位置：本机 ~/.hermes/.env（不进 git）；模板 materials/hermes/.env.template
```

------

## 5. 文档资产约定

| 文件 | 谁维护 | 何时更新 |
| --- | --- | --- |
| `memory/kit/MEMORY.md` | 人定型，Agent 同步快照/约束 | 某阶段一句话变了，或约束/入口变了 |
| `memory/kit/ENVIRONMENT.md` | 人为主 | **仅当**服务对象真实办事方式变了 |
| `memory/kit/REQUIREMENTS.md` | 人定稿条目，Agent 改状态 | 需求讨论定稿、条目增删、对照验收打状态 |
| `memory/kit/FRAMEWORK.md` | 人定型，Agent 同步选型/模块 | 框架讨论定稿或选型/模块变更 |
| `memory/kit/FLOW.md` | 人定型，Agent 同步链路 | 实现流程定稿或端到端怎么走变了 |
| `memory/kit/TODO.md` | Agent 随任务 | 大任务开始/完成打钩。**每条要有可判定的验收**（写不出 ⇒ 还不是待办）；已知限制归 HANDOVER，不进 TODO；结构约定见模板 |
| `memory/kit/ITERATION.md` | Agent | 目的/范围/条目/框架/链路变更时追加 |
| `memory/kit/annex/*.md` | Agent | **代码实现后的交付**新建一份 `VERIFY-`；**一天做成多件事**再加一份 `INDEX-YYYYMMDD.md` 串起来（只放指针）；小改动不强制；**里程碑后旧 VERIFY / INDEX 归档 `annex/_archive/`** |
| `memory/kit/HANDOVER.md` | 人为主，Agent 随任务 | **跨阶段必知事实**（环境 / 路径 / 账号位置 / 工具版本 / 结论 / 坑 / 已排除的路）；**行内改，可增删**（≠ ITERATION 只追加）；改完刷新该条「核实日期」**与顶部「最后核实」**并追加一行 `ITERATION.md` |
| `memory/kit/REFERENCES.md` | 人为主，Agent 随任务 | **外部对标 / 外部系统 / 来源的地址簿**；**行内改，可增删**；**只放指针**，原文摘录 / 提示词 / 阈值另写 `annex/NOTE-YYYYMMDD-短名.md`；不再用的条目**直接删** |
| 项目根 `AGENTS.md` | Init 由 `templates/AGENTS.md` 生成 | Claude Code / 非 Cursor Agent 的**常驻管理文件**；不读 `.cursor` 的 Agent 以它为准 |
| `.cursor/rules/project-memory.mdc` | Init 由 `templates/cursor-rule.mdc` 生成 | Cursor 的**常驻规则**（alwaysApply，每轮注入） |
| Skill `references/` | 不拷进本仓库 | 按需打开（规则见下方）；日常编码不要读 |

> **本记忆按 kit v1.3.1 建立。** 判断该不该跟版：读 kit `SKILL.md` 顶部的 `kit-version` / `kit v…` 与本行比对，不同则按 `references/migration.md` 的「二、骨架升级」补齐，改完把本行版本号更新。

### 阅读策略（默认只读 MEMORY）

日常改代码：**只读 `MEMORY.md`。** 不要每个任务把 `memory/kit/` 全部打开，也不要打开 Skill / `references/`。
同一会话里 MEMORY 已读过且文件没改，不必每轮重读全文。打开源文件是为了澄清，不要把正文粘回 MEMORY。

**阶段源文件（快照不够再打开）**

| 这时才打开 | 文件 |
| --- | --- |
| 对照 R1、R2 或勾验收状态 | `REQUIREMENTS.md` |
| 模块 / 选型不够 | `FRAMEWORK.md` |
| 端到端怎么走不够 | `FLOW.md` |
| 服务对象现状不够 | `ENVIRONMENT.md` |
| 环境 / 路径 / 账号位置 / 命令 / 已知的坑不够 | `HANDOVER.md`（**事实仅供参考，用前核实未过时**） |
| 要对标某个外部产品 / 查外部系统怎么接 / 找参考实现 | `REFERENCES.md`（**只放地址；研究正文是 `annex/NOTE-…`**） |

**TODO、待办、交付记录、变更史**

| 这时 | 做什么 |
| --- | --- |
| 开始或接续大任务、看进度、打钩 | 打开 `TODO.md`（进行中 / 待办 / 已完成） |
| 一次性聊天里的零碎清单 | **不要**写入 TODO；TODO 只留项目级待办 |
| **代码实现后要交付 / 验收** | 新建 `memory/kit/annex/VERIFY-YYYYMMDD-任务名.md`（模板 `VERIFY.md`） |
| **一天做成多件事** | 每件事各写一份 `VERIFY-…`；再建 `annex/INDEX-YYYYMMDD.md`（从 `_INDEX.md` 复制改名；**只放指针**；一天一事就不建） |
| 小改动、改文案、明确小 bug | 不强制写 VERIFY |
| 续做同一任务、或用户问上次怎么验 | 只打开**那一份** VERIFY，不要读完全部 `annex/` |
| 查或记「为什么变成现在这样」 | 打开 / 追加 `ITERATION.md` |

**Skill `references/`（不在本仓库）**

位置：本机安装的 `%USERPROFILE%\.claude\skills\project-memory-kit\references\`（Cursor 下为 `%USERPROFILE%\.cursor\skills\...`）。
权威源：[github.com/RedOctupus/ai-agent-config-live](https://github.com/RedOctupus/ai-agent-config-live) 的 `materials/agent-skills/`。

| 这时才打开 | 文件 |
| --- | --- |
| 用户说 init / 初始化项目记忆 | 该 Skill 的 `SKILL.md` + `templates/` |
| 大任务定型、Ask / Plan、讨论顺序不清 | `references/collaboration.md` |
| 不确定改法、高风险、测试汇报怎么写 | `references/agent-rules.md` |
| 用户点名要工程脚手架 | `references/scaffold.md` |
| 已有 `memory/kit/` 但不符合本骨架（存量收敛） | `references/migration.md` |
| 项目有多个维护者 / 多模块 | `references/team.md` |

禁止：为了「保险」每个任务都把 references 读一遍；禁止把 references 拷进业务项目。

### MEMORY 体量（防爆炸）

MEMORY 只保留各阶段**当前一句话**和编码门闸（约束、入口），不是源文件副本。

| 写这里 | 不要写这里，写到 |
| --- | --- |
| 大环境一句话 | 对方怎么办事的正文 → `ENVIRONMENT.md` |
| 需求目的一句话 | 拆开的条目、验收句 → `REQUIREMENTS.md` |
| 框架骨架一句话 | 选型、模块表、分层 → `FRAMEWORK.md` |
| 实现流程一句话 | 步骤、分支、每步 I/O → `FLOW.md` |
| 约束与入口（短） | 函数、参数、schema → 代码；步骤/待办 → `TODO.md`；验证记录 → `annex/`；变更史 → `ITERATION.md` |
| 必知事实（只留指针，见 §0） | 环境 / 路径 / 账号位置 / 工具版本 / 结论 / 坑 → `HANDOVER.md` |
| 外部地址（只留指针，见 §0） | 对标产品文档 / 外部服务端点与本机路径 / 参考仓库 → `REFERENCES.md` |

规则：

- **改写快照，不堆历史。** 源文件改了，只在某阶段一句话变了时改本表；小改动若各阶段一句话和约束都没变，**不要**动 MEMORY。
- **超了就外移。** 单节 >40 行删细节留文件名；全文 >400 行走下方裁剪门闸。
- **§0 只数实义行。** 配额是 **≤ 15 行实义内容 / ≤ 900 字符**，**单行 ≤ 300 字符**。空行、标题、`>` 说明块**不计**。
- **每个文件最多链一次。** 后续提及用反引号文件名。
- **战报不进 MEMORY。** → `annex/` 各 VERIFY。
- **取证不入库。** 截图 / 原始 JSON / stdout → `memory/kit/annex/_raw/`。

**裁剪门闸：** 跑 `python scaffold/scripts/check-memory-size.py`。

------

## 6. 协作口令（人用）

```text
【大环境】对齐服务对象大环境：对方现在怎么办事。写入 ENVIRONMENT；MEMORY 只留一句话。
【需求讨论】目的 / 约束 / 验收 / 不做。定稿后写入 REQUIREMENTS 条目，MEMORY 只留一句话目的。
【框架讨论】需求条目已定。框架建立在各技术栈选择上：**每一项**先给候选和取舍，等用户明确同意再写入 FRAMEWORK。禁止自行拍板。
【实现流程】框架已定。端到端数据怎么走、分支与每步 I/O 写入 FLOW，MEMORY 只留链路一句话。
【Plan】文件、步骤、验证；TODO 对应 REQUIREMENTS 的 ID
【对照开发】按 R1、R2… 做，验收勾 REQUIREMENTS 状态
【Agent】按 Plan 最小修改
【验收】给命令和预期输出
【叫停】先别写代码，回到大环境或需求或框架或实现流程
```

大任务：大环境 → 需求讨论（REQUIREMENTS）→ 框架讨论（FRAMEWORK）→ 实现流程（FLOW）→ Plan → Agent。

------

## 7. 阅读完成门闸（Agent）

编码前必须能回答，否则继续读、禁止编码：

1. 本项目要达成的目的是什么？（第 2 节需求目的；条目打开 REQUIREMENTS）
2. 当前改动属于哪个模块？（第 2 节框架快照；细节打开 FRAMEWORK）数据怎么走？（第 2 节实现流程快照；细节打开 FLOW）
3. 风险与最小修改、怎么验？（第 3–4 节）
4. 不要把源文件正文粘进 MEMORY。
5. 不要为答门闸而把全部 memory 文件读一遍；只打开当前不够的那一份。
6. **大任务**要进 Plan 或写代码时：`FRAMEWORK.md` 仍空 → 先提醒【框架讨论】；`FLOW.md` 仍空 → 先提醒【实现流程】。用户书面确认跳过、或声明这是小任务后，才可以动手。
7. **技术选型硬阀门：** 框架未立或某技术栈用户未点头 → 禁止写入「已定」、禁止按该栈编码。先列出待选，逐项等确认。建议不等于已定。
8. 交付时写 VERIFY；打钩看 TODO。不要为答门闸去读完全部 `annex/` 或 Skill `references/`。
9. **碰环境 / 路径 / 账号 / 命令前：** 先看 `HANDOVER.md`，并核对它的「核实日期」与顶部「最后核实」没过时。那里的事实**仅供参考**，用前核实；与现场冲突以现场为准。
