# 项目记忆（人 + Agent 共用）

> 各阶段的**简化快照**（门闸索引）。只留基础信息，不写源文件正文。
> 需要澄清时打开对应源文件。Agent 改代码前必须能回答文末「阅读完成门闸」。

------

## 0. 交接清单（可选 · ≤ 15 行）

> 给无上下文的新 Agent 5 分钟交接。**只放指针和一句话结论，禁放逐轮战报、逐缺陷状态、E2E 明细**——那些回 `tests/` 各 TEST-LOG。

- **项目是什么：**（一句话）
- **当前进度：**（一句话 + 关键数字）
- **端到端 / 测试覆盖：** 一行一个 TEST-LOG 指针（细节回 `tests/`）
- **已拍板（跨线规则）：** 一行一条，只留结论
- **工作分支：** 分支名 + HEAD（HEAD 易腐：大任务开始前 `git rev-parse --short HEAD` 校准；不确定就只留分支名）

**正反例（只留指针，不贴正文）：**

| ❌ 坏（贴正文进 §0） | ✅ 好（一句话 + 指针） |
| --- | --- |
| `多轮对话三缺陷：RAG 只用当前消息……逐条 +90/−20` | `多轮对话三缺陷：见 [ITERATION](ITERATION.md)` |
| `E2E 第 5 轮 137/6 逐用例结论…` | `E2E 补测：见 [TEST-LOG](tests/…)` |

------

## 1. 项目简介

- **名称：**
- **当前阶段：** MVP / Beta / Production / Maintenance / 学习作业
- **当前优先级：** 稳定性 / 交付速度 / 成本 / 扩展性

------

## 2. 阶段快照

未讨论的阶段保持空白，不要编造。一句话变了才改这里；细节只改源文件。

| 阶段 | 当前一句话 | 源文件 |
| --- | --- | --- |
| 服务对象大环境 |  | `ENVIRONMENT.md` |
| 需求目的 |  | `REQUIREMENTS.md` |
| 项目框架 |  | `FRAMEWORK.md` |
| 实现流程 |  | `FLOW.md` |

------

## 3. 约束

**硬阀门：技术选型（框架讨论）**

框架的确立**基于各技术栈的选择**。库、中间件、语言/框架、存储、向量库、解析器、第三方服务等，**每一项**都必须先和用户商量，得到明确同意后，才能写入 `FRAMEWORK.md`、改 MEMORY 框架快照、或据此写代码 / 进实现流程 / Plan。

禁止：自行拍板、拿常见方案当已定、把「建议」写成「用什么」、未确认就新增依赖。未确认的项只能放在「待商量」，不能当框架已立。

**禁止触碰：**

```text
（路径或模块；无则写「无」）
```

**高风险（改前需确认）：** 数据库结构、权限/认证、部署配置、生产环境变量、删除数据。

**开发开关：**

| 项 | YES / NO |
| --- | --- |
| 允许新增依赖 |  |
| 允许重构 |  |
| 允许改表 / schema |  |
| 允许改接口协议 |  |

**特殊规则：**

```text
（容易误解的规则、必须遵守的原则）
```

------

## 4. 入口与运行

```text
关键文件：
如何启动：
配置位置：（例如 .env，勿把密钥写入本文件）
```

------

## 5. 文档资产约定

| 文件 | 谁维护 | 何时更新 |
| --- | --- | --- |
| `docs/memory/MEMORY.md` | 人定型，Agent 同步快照/约束 | 某阶段一句话变了，或约束/入口变了 |
| `docs/memory/ENVIRONMENT.md` | 人为主 | **仅当**服务对象真实办事方式变了 |
| `docs/memory/REQUIREMENTS.md` | 人定稿条目，Agent 改状态 | 需求讨论定稿、条目增删、对照验收打状态 |
| `docs/memory/FRAMEWORK.md` | 人定型，Agent 同步选型/模块 | 框架讨论定稿或选型/模块变更 |
| `docs/memory/FLOW.md` | 人定型，Agent 同步链路 | 实现流程定稿或端到端怎么走变了 |
| `docs/memory/TODO.md` | Agent 随任务 | 大任务开始/完成打钩。只留项目级进行中/待办/已完成，不堆聊天清单 |
| `docs/memory/ITERATION.md` | Agent | 目的/范围/条目/框架/链路变更时追加 |
| `docs/memory/tests/*.md` | Agent | **代码实现后的交付**新建一份；小改动不强制；**里程碑后旧 TEST-LOG 归档 `tests/_archive/`** |
| 项目根 `AGENTS.md` | Init 由 `templates/AGENTS.md` 生成 | Claude Code / 非 Cursor Agent 的**常驻管理文件**；不读 `.cursor` 的 Agent 以它为准 |
| `.cursor/rules/project-memory.mdc` | Init 由 `templates/cursor-rule.mdc` 生成 | Cursor 的**常驻规则**（alwaysApply，每轮注入） |
| Skill `references/` | 不拷进本仓库 | 按需打开（规则见下方）；日常编码不要读 |

> **编辑器部署：** 本 Skill 部署到 **Cursor** 落在 `.cursor/rules/project-memory.mdc`（rules，每轮注入）；**Claude Code** 等不读 `.cursor` 的 Agent 用项目根 `AGENTS.md` 作**等价管理文件**。两者同源，都只做「读 `docs/memory/MEMORY.md` + 门闸提醒」，正文仍只在 `docs/memory/`。

### 阅读策略（默认只读 MEMORY）

日常改代码：**只读 `MEMORY.md`。** 不要每个任务把 `docs/memory/` 全部打开，也不要打开 Skill / `references/`。
同一会话里 MEMORY 已读过且文件没改，不必每轮重读全文。打开源文件是为了澄清，不要把正文粘回 MEMORY。

**阶段源文件（快照不够再打开）**

| 这时才打开 | 文件 |
| --- | --- |
| 对照 R1、R2 或勾验收状态 | `REQUIREMENTS.md` |
| 模块 / 选型不够 | `FRAMEWORK.md` |
| 端到端怎么走不够 | `FLOW.md` |
| 服务对象现状不够 | `ENVIRONMENT.md` |

**TODO、待办、测试、变更史**

| 这时 | 做什么 |
| --- | --- |
| 开始或接续大任务、看进度、打钩 | 打开 `TODO.md`（进行中 / 待办 / 已完成） |
| 一次性聊天里的零碎清单 | **不要**写入 TODO；TODO 只留项目级待办 |
| **代码实现后要交付 / 验收** | 新建 `docs/memory/tests/YYYYMMDD-任务名.md`（用 `_TEMPLATE.md`） |
| 小改动、改文案、明确小 bug | 不强制写测试日志 |
| 续做同一任务、或用户问上次怎么验 | 只打开**那一份**测试日志，不要读完全部 `tests/` |
| 查或记「为什么变成现在这样」 | 打开 / 追加 `ITERATION.md` |

**Skill `references/`（不在本仓库）**

位置：`%USERPROFILE%\.cursor\skills\project-memory-kit\references\`，或治理框架工作区里的同名目录。

| 这时才打开 | 文件 |
| --- | --- |
| 用户说 init / 初始化项目记忆 | 该 Skill 的 `SKILL.md` + `templates/` |
| 大任务定型、Ask / Plan、讨论顺序不清 | `references/collaboration.md` |
| 不确定改法、高风险、测试汇报怎么写 | `references/agent-rules.md` |
| 用户点名要工程脚手架 | `references/scaffold.md` |
| 已有 `docs/memory/` 但不符合本骨架（存量收敛） | `references/migration.md` |
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
| 约束与入口（短） | 函数、参数、schema → 代码；步骤/待办 → `TODO.md`；验证记录 → `tests/`；变更史 → `ITERATION.md` |

规则：

- **改写快照，不往节末堆历史。** 源文件改了，只在一句话变了时改本表。
- **超了就外移。** 单节超过约 40 行：删细节，留源文件名。
- **全文建议不超过约 200 行。**
- 小改动若各阶段一句话和约束都没变：**不要**改 MEMORY。
- **测试 / 验收战报不进 MEMORY。** E2E 逐轮结果、逐缺陷状态、复跑取证 → 写 `tests/` 各 TEST-LOG；MEMORY（含 §0）只留一句「见 [TEST-LOG](...)」指针。
- **测试取证不入库。** 截图 / 原始 JSON / stdout / SQL 快照 → 放 `tests/*/_raw/`，并在 `.gitignore` 加 `docs/memory/tests/*/_raw/shots/`；只提交手写的 TEST-LOG `.md`。

**裁剪门闸（超了就裁，别等它自己瘦）：**

触发：`python scripts/check-memory-size.py` 报超阈值（全文 >200 行 / §0 >15 行），或单节明显超 40 行。

怎么裁（只外移，不删除）：
1. 逐轮战报 / 逐缺陷状态 / E2E 明细 → 回 `tests/` 各 TEST-LOG，MEMORY 只留指针。
2. 模块 / 仓库地图 / 文件索引 → 挪到 `FRAMEWORK.md`。
3. 源文件正文 → 删掉，留源文件名。
4. 已过里程碑的正文 → 挪到 `ITERATION.md`（变更史）。
5. 裁完再跑一次 check，达标再动手。

------

## 6. 协作口令（人用）

```text
【大环境】对齐服务对象大环境：对方现在怎么办事。写入 ENVIRONMENT；MEMORY 只留一句话。
【需求讨论】目的 / 约束 / 验收 / 不做。定稿后写入 REQUIREMENTS 条目，MEMORY 只留一句话目的。
【框架讨论】需求条目已定。框架建立在各技术栈选择上：**每一项**先给候选和取舍，等用户明确同意再写入 FRAMEWORK。禁止自行拍板。能力模块、分层同样先商量。先不定逐步怎么走，更不定代码。
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
8. 交付时写测试日志；打钩看 TODO。不要为答门闸去读完全部 `tests/` 或 Skill `references/`。
