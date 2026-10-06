---
name: project-memory-kit
metadata:
  kit-version: "1.7.1"
description: >-
  Initializes and maintains compact project memory for humans and agents.
  Use when the user says init a new project, 初始化项目记忆, 新建项目脚手架,
  or when a repo already has docs/memory/ and the task changes requirements,
  requirement breakdown, architecture, TODOs, 服务对象大环境, 项目框架, 实现流程,
  or needs an annex VERIFY / NOTE / CHECKLIST / INDEX.
  Use the business-context-first Agent design workflow when the task adds or changes Agents, capability modules, role views, multi-Agent coordination, memory behavior, or cross-domain business flows. For Agent-to-Agent work, the design must record the collaboration contract before implementation; Agent↔module reuse is many-to-many.
---

# Project Memory Kit

> **kit v1.7.1** —— 项目侧应在自己的 `MEMORY.md` §5 记下「按哪个版本建立」，用于判断是否该按 [references/migration.md](references/migration.md) 的「二、骨架升级」跟版。

人读 [README.md](README.md)。Agent 以本文件为准。

人机共用上下文：MEMORY 快照 + ENVIRONMENT / REQUIREMENTS / FRAMEWORK / FLOW 源文件 + 迭代 / TODO / 交付记录（annex）。行事哲学原文不拷进项目。

## 路径约定

Init 后新项目：

```text
docs/memory/MEMORY.md       # 各阶段一句话快照、约束、入口
docs/memory/ENVIRONMENT.md  # 服务对象大环境（现状）
docs/memory/REQUIREMENTS.md # 拆解条目，对照开发
docs/memory/FRAMEWORK.md    # 项目框架：选型、能力模块、分层
docs/memory/FLOW.md         # 实现流程：端到端怎么走
docs/memory/BUSINESS-CONTEXT.md # Agent / 复杂业务上下文索引（L2/L3 可选）
docs/memory/TODO.md
docs/memory/ITERATION.md
docs/memory/HANDOVER.md     # 跨阶段必知事实（可增删改，非追加）
docs/memory/REFERENCES.md   # 外部对标 / 外部系统 / 来源的地址簿（可增删改）
docs/memory/annex/VERIFY-YYYYMMDD-任务名.md   # 外移夹：VERIFY / NOTE / CHECKLIST / INDEX-YYYYMMDD / _raw
docs/memory/annex/_INDEX.md                 # 当日索引模板（真下发文件名是 INDEX-YYYYMMDD.md）
AGENTS.md
.cursor/rules/project-memory.mdc
```

本 Skill 目录：`templates/` 可拷贝；`references/` 不拷进项目，按需再读。

- 业务上下文优先的 Agent 设计：加载独立 `business-context-first-agent-design` Skill；Kit 只负责项目内落点和路由
- 协作 / 模式选择：[references/collaboration.md](references/collaboration.md)
- 阅读、最小修改、测试汇报：[references/agent-rules.md](references/agent-rules.md)
- MVC 与工程骨架：[references/scaffold.md](references/scaffold.md)
- 存量项目收敛：[references/migration.md](references/migration.md)
- 多人 / 多模块维护：[references/team.md](references/team.md)

## 本 Skill 何时打开（不是日常阅读策略）

日常改代码**不会**读这份 SKILL。何时读 TODO / annex / 源文件 / `references/`：**以项目里 `MEMORY.md` 第 5 节为准。**

本 SKILL 只在这些时候打开（与 MEMORY 第 5 节「Skill references」一致）：

| 情况 | 读 |
| --- | --- |
| 用户说 init / 初始化项目记忆 | 本 SKILL + `templates/` |
| 大任务定型、Ask/Plan | [references/collaboration.md](references/collaboration.md) |
| 不确定改法、怎么验 | [references/agent-rules.md](references/agent-rules.md) |
| 用户点名工程脚手架 | [references/scaffold.md](references/scaffold.md) |
| 已有 memory 但不符合骨架（收敛），或 kit 升级后老项目要跟版 | [references/migration.md](references/migration.md) |
| 项目有多个维护者 / 多模块 | [references/team.md](references/team.md) |

## Init（用户说 init 新项目 / 初始化项目记忆）

目标目录：当前工作区根；若用户指定了路径，用用户路径。

### 初始化前的两个独立选择

Kit 的**单人 / 多人**维护模式与**AOCI 源码地图：启用 / 不启用**是两个独立选择。单人模式默认不强制选择：用户独自 clone 项目即可用 Kit，不必先回答工作区问题；只有明确多人维护或结构无法判断时才问维护模式。AOCI 仍须用户明确启用；未答时不安装，MEMORY 标为“未启用／待确认”。不因多人默认启用 AOCI，也不因 AOCI 改多人骨架。

**单人 clone 本身就是可用工作区**，不强制创建 worktree；用户主动并行开发时才考虑独立 worktree。多人模式则在根 `ROOT-MEMORY.md` 记录人类确认的集成分支；不能猜 `main` 或 `master`。新人 clone 后先由项目入口提醒工作区准入，集成分支检出目录不直接写源码。独立 clone 的功能分支或 linked worktree 均可作为工作区；不得静默创建。

用户选择不启用：保留目标 MEMORY 的“未启用”状态，**不得运行 aoci init**，不配置项目级 MCP；日常仍直接核对源码和测试，按 Kit §5 回写。用户确认启用后：先核对 AOCI 版本、许可、宿主与安装来源，遵守各项技术选型确认；AOCI 是项目级 stdio MCP，Kit 本身是 Skill，不是第二个 MCP。按当前 AOCI 官方安装说明在**目标 Git 仓**配置所选宿主，不覆盖既有配置；宿主配置含本机绝对路径，必须忽略且每台机器分别配置。再按当前机器 Guide 决定 Scope、scan 和模型编写索引，不把 AOCI 的执行状态机复制进 Kit。

**本仓安装来源优先：** 已安装时先读 `~/.local/share/ai-agent-config/memory-tools.json` 的 `source_repo` / `aoci.binary`，复用校验过的本机 AOCI。为当前工作区注册 MCP，用该源仓的 `scaffold/scripts/install-memory-tools.py configure --repo <绝对 Git 根> --hosts <当前宿主> --apply`；注册后再按当前 AOCI init/Guide 建图。没有本机定位时先询问本仓 clone 路径，按仓内 `materials/tools/aoci/README.md` 安装；**init 不自动从 AOCI GitHub 下载**。仅明确要替换既有 AOCI 配置时才用 `--replace-aoci`。包来源与版本集中由源仓维护，Kit 不复制二进制。

单人项目由 `docs/memory/MEMORY.md` 的 `kit:aoci-status` 行负责状态；多人项目由架构负责人维护根 `ROOT-MEMORY.md` 的同名状态，模块 MEMORY 只指向根状态，不各自宣布启用。启用状态只在 MCP 可用且正式索引对齐后写入；仅装二进制或配置 MCP 不等于已启用。

1. 若目标已有 `docs/memory/MEMORY.md`：结构不合骨架（缺源文件 / 超长 / 战报堆正文）→ 走 [references/migration.md](references/migration.md) 收敛；结构已合则只补缺文件、不覆盖。
2. 从本 Skill 的 `templates/` 与 `scripts/` 拷贝（本 SKILL.md 所在目录为 kit 根）：

| 源 | 目标 |
| --- | --- |
| `templates/MEMORY.md` | `docs/memory/MEMORY.md` |
| `templates/REQUIREMENTS.md` | `docs/memory/REQUIREMENTS.md` |
| `templates/FRAMEWORK.md` | `docs/memory/FRAMEWORK.md` |
| `templates/FLOW.md` | `docs/memory/FLOW.md` |
| `templates/TODO.md` | `docs/memory/TODO.md` |
| `templates/ENVIRONMENT.md` | `docs/memory/ENVIRONMENT.md` |
| `templates/BUSINESS-CONTEXT.md` | `docs/memory/BUSINESS-CONTEXT.md`（仅 Agent / 复杂业务 L2/L3；已有则不覆盖） |
| `templates/ITERATION.md` | `docs/memory/ITERATION.md` |
| `templates/HANDOVER.md` | `docs/memory/HANDOVER.md` |
| `templates/REFERENCES.md` | `docs/memory/REFERENCES.md` |
| `templates/annex/_TEMPLATE.md` | `docs/memory/annex/_TEMPLATE.md`（选哪种） |
| `templates/annex/VERIFY.md` | `docs/memory/annex/VERIFY.md` |
| `templates/annex/NOTE.md` | `docs/memory/annex/NOTE.md` |
| `templates/annex/CHECKLIST.md` | `docs/memory/annex/CHECKLIST.md` |
| `templates/annex/_INDEX.md` | `docs/memory/annex/_INDEX.md`（当日索引**模板**；真下发是 `INDEX-YYYYMMDD.md`） |
| `scripts/check-memory-size.py` | `scripts/check-memory-size.py`（体量门闸；AGENTS.md / MEMORY 按**项目内相对路径**调用它，故须随 init 落地，否则那条命令在项目根直接失败） |
| `scripts/kit-workspace.py` | `scripts/kit-workspace.py`（仅多人源码写入前做工作区状态检查；显式 `create` 才创建 worktree；单人可直接用 clone） |
| `templates/AGENTS.md` | 项目根 `AGENTS.md`（已有则合并指针，不抹掉用户原文） |
| `templates/cursor-rule.mdc` | `.cursor/rules/project-memory.mdc` |
| `templates/gitignore-memory.txt` | 项目根 `.gitignore`（把内容**追加**进去——已有 `.gitignore` 时不要覆盖） |

多模块 / 多人：走 [references/team.md](references/team.md)；根索引用 `templates/ROOT-MEMORY.md`、认领表用 `templates/OWNERS.md`，模块子目录复用上表单项目模板。**将模块 MEMORY 的默认 AOCI 状态行替换为指向根 ROOT-MEMORY.md 的指针**（保留 `kit:aoci-status` 标记，用相对路径）；模块不得保留单人模板的“未启用”结论，也不得各自声明项目级 MCP 已启用。

3. 只填 MEMORY 里立刻知道的项（文件夹名、当前阶段若用户已说）。其余留空，不编造业务。
4. **老项目补句**：目标已有 `AGENTS.md` 或 `.cursor/rules/project-memory.mdc` 时（常见于早先 init 的项目），除合并指针外，**逐句对照本 kit 的 `templates/AGENTS.md` 与 `templates/cursor-rule.mdc`**，缺哪句补哪句。两处都是每轮注入，**必须同时改**——只改一处，不读 `.cursor` 的 Agent 就漏了。

   **清单以 templates 为准，本 SKILL 不枚举。** 曾经的枚举会随模板升级变旧：HANDOVER 那次就是因为这份清单没跟上模板，老项目永远补不进新增的维护口令。典型必带句（**举例，非清单**）：「**改完就同步记忆，别等用户问**」、「大任务开始前先跑 `python scripts/check-memory-size.py`」。

   只补缺句，不重写用户原文。
5. **默认只 init 记忆目录 + 体量门闸脚本。** 仅当用户明确要工程脚手架时，再按 `references/scaffold.md` 生成 `.gitignore`、`.env.example`、`README.md` 骨架。不要默认生成 RBAC、JWT、Docker。
6. 向用户汇报创建了哪些路径。

## 日常维护（已 init）

### 工作区隔离、集成与 AOCI

工作区不等于人员或模块：它是有独立绝对根路径的**独立 clone 或 Git worktree**。同一人可有多个工作区，同一模块也可由不同工作区先后修改。`OWNERS.md` 仍管业务模块责任，不把 owner 表当作 worktree 清单。Git 状态能识别分支和 worktree，但**不能从 Git 状态证明没有其他 Agent 同时写该目录**；多人并行仍须约定一个工作区同一时刻只有一个写入者。

多人源码任务前读根 `ROOT-MEMORY.md` 的集成分支，再运行 `python scripts/kit-workspace.py status --repo . --mode team --integration-branch <已确认分支>`。功能分支 clone/worktree 已可用时不重复创建；集成分支检出目录只读，不在此开发。需要新目录时先征询用户路径、分支和基线，再显式运行 `create`；不静默创建，也不自动复制本机 MCP 配置或 AOCI 运行状态。每个 AOCI 启用的工作区必须按当前版本官方接入说明单独校验 `--repo` 指向和地图治理，不能把另一个工作区的绝对路径配置当成可移植资产。单人项目默认不做此团队准入检查，当前 clone 可直接工作。

个人 AOCI 地图只作为集成提案：分支可提交索引差异供审查，但**不得文本合并个人 aoci.code.txt** 到主分支。集成负责人串行处理，**先合并源码，再对合并后的源码重新签发**当前 AOCI 候选、核实个人提案与真实源码、写入全局 Entry，并依当前 Guide 完成 Verify/Check/Guide；源码与全局图对齐后才交付集成。个人候选的 SHA、batch、candidate ID 不能跨工作区重放；同一对象冲突、Meta/Scope 不兼容、证据不足或治理未对齐时停在人工裁决，不靠词句拼接或强制覆写。

Kit 不内嵌 AOCI 版本和状态机：Kit 只负责是否启用、工作区准入、源码任务触发和 Kit 槽位回写；工具格式、认知建立与写入步骤取当前 MCP/Guide。AOCI 不可用不等于未启用：已启用时标记待维护、不能宣称闭环。独立更新 Kit 或 AOCI 时先做能力/宿主配置兼容检查，**不得自动升级 AOCI**，也**不得自动覆盖宿主配置**或本机已装 Kit；不兼容时保留源码/Kit 工作并报告阻断点。

### 源码任务与 AOCI

**仅启用 AOCI 的源码任务**：Kit `MEMORY.md` 的状态指针引到项目根 `AGENTS.md` 的 AOCI 区块；先依当前服务取得 `aoci_rules` 与完整 `aoci_overview`，Overview 交付确认只用本次返回的 `delivery_receipt_version`，不得猜协议版本；再按任务取 Entry 并回真实源码/测试核实。纯非代码任务不机械调用；只读源码且没有受管变更时不调用 Maintain。**最终代码和测试稳定后**依当前 MCP/Guide 调 `aoci_maintain` 并完成模型撰写的受影响 Entry，按返回命令依次 `verify → check → Guide` 证明对齐；随后同轮落 Kit VERIFY/ITERATION 及 §5 指定的其他槽位。AOCI 只管代码地图，不能把源码中出现的技术当作用户已确认选型，也不替代源码、测试或人审。

已启用项目若 AOCI 不可用、冲突或无法对齐：可以继续用 Kit＋源码/测试做受限工作，但必须在交付中标出 AOCI 待维护，**不得宣称代码交付闭环完成**；不能静默把旧 Entry 当当前证据。未启用项目按 MEMORY 中“未启用”提示走 Kit-only，不制造待维护负债。

### Agent / 复杂业务设计路由

Kit 不动态执行另一个 Skill；它通过项目入口规则路由：涉及新增或修改 Agent、能力模块、角色视图、多 Agent 协作、记忆读写或跨业务域流程时，先加载 `business-context-first-agent-design`。Kit 项目优先使用 `docs/memory/BUSINESS-CONTEXT.md`，不要创建平行的 `agent-design/` 记忆树。没有 Kit 的项目由该独立 Skill 以兼容模式使用 `docs/agent-context/`。

当任务级别为 L0/L1 时只检查受影响的上下文；L2/L3 时先完成业务域 → 生命周期 → 角色任务 → 上下文 → Agent → 原子能力 → 能力模块 → 角色视图 → 跨域回流门闸。

不是 Cursor 出厂默认；依赖项目里的 `project-memory.mdc`。按任务规模更新：

| 事件 | 动作 |
| --- | --- |
| 大任务开始 | 对齐 `ENVIRONMENT.md`；需求写入 `REQUIREMENTS.md`；框架写入 `FRAMEWORK.md`（**每一项技术栈须用户确认后才能当作已定**）；实现流程写入 `FLOW.md`；MEMORY 只改对应一句话；再更新 `TODO.md`；**先跑 `python scripts/check-memory-size.py` 校验体量（超阈值先裁剪）**。§0「工作分支」只留分支名，不要刷短哈希 |
| 需求讨论定稿或条目增删 | 改 `REQUIREMENTS.md`；目的一句话变了才改 MEMORY 快照；追加 `ITERATION.md` |
| 选型或模块变更 | 先与用户确认该技术栈；再改 `FRAMEWORK.md`；骨架一句话变了才改 MEMORY 快照；追加 `ITERATION.md` |
| 实现流程变更 | 改 `FLOW.md`；链路一句话变了才改 MEMORY 快照；追加 `ITERATION.md` |
| 交付 / 验收相关改动 | 新建 `docs/memory/annex/VERIFY-YYYYMMDD-任务名.md`（模板 `VERIFY.md`） |
| 服务对象**真实办事方式**变了 | 才更新 `ENVIRONMENT.md`；大环境一句话变了才改 MEMORY 快照 |
| 发现 / 修改**跨阶段必知事实**（环境、路径、账号位置、工具版本、研究结论、坑、已排除的路） | 改 `HANDOVER.md`（**行内改，可增删**，不是追加）；刷新该条「核实日期」与顶部「最后核实」；追加一行 `ITERATION.md`（影响写 `HANDOVER.md`）；MEMORY 不动 |
| 新增 / 删除**外部对标、外部系统、来源地址**（对标产品文档、外部服务端点与本机路径、参考仓库 @ commit） | 改 `REFERENCES.md`（**行内改，可增删**）；研究正文另写 `annex/NOTE-YYYYMMDD-短名.md`、这里只留指针；追加一行 `ITERATION.md`（影响写 `REFERENCES.md`）；MEMORY 不动 |
| 项目里程碑 | 源文件若变了就改源文件；MEMORY 只改变了的那句快照；追加 `ITERATION.md`；**默认不改大环境** |
| 一天做成多件事 | 每件事各写一份 `annex/VERIFY-…`；再建一份 `annex/INDEX-YYYYMMDD.md` 串起来（**只放指针，禁贴正文**；一天只有一件事就不建） |
| 小改动 | 仅当状态变化时改 MEMORY/TODO；不强制写源文件或 VERIFY |

更新 MEMORY 时：**只改快照一句话和约束/入口，禁止往里粘源文件正文。** 变更记录只追加 `ITERATION.md`。详见 MEMORY 模板「体量」节。

交付 / 验收：新建 `annex/VERIFY-YYYYMMDD-任务名.md`；研究摘录用 `NOTE-`；手工步骤用 `CHECKLIST-`。逐轮结果、逐缺陷状态、复跑取证只进 `annex/`，**不进 MEMORY**；截图 / 原始 JSON / stdout 放 `docs/memory/annex/_raw/`，`.gitignore` 加同名路径，只提交手写 `.md`（`annex/` 若按任务分子目录，则用 `docs/memory/annex/*/_raw/`）。

**不**在日常任务里创建行事哲学 01~05、`references/` 副本、额外哲学文档。

缺约定文件（被删或 init 不完整）：

1. 只补 **templates 里的同名路径**，不发明新文件名。
2. **先查 git / 对话里是否还有旧内容**；有则恢复旧内容，不要用空模板盖掉进度。
3. 只有确认无旧内容时，才从 `templates/` 拷一份空白模板。
4. 若不得不用模板覆盖：必须先告诉用户「会丢掉该文件里的打钩/正文」，得到确认再拷。
5. 若项目里仍是旧名 `MANUAL.md`：重命名为 `ENVIRONMENT.md`，不要两份并存。

`ITERATION.md` 追加时分清两类（「影响」列写清）：

- 某阶段一句话 / 约束 / 入口 → 影响 MEMORY
- 服务对象真实办事方式 → 影响 ENVIRONMENT
- 具体需求条目 → 影响 REQUIREMENTS
- 选型 / 能力模块 / 分层 → 影响 FRAMEWORK
- 端到端怎么走 → 影响 FLOW
- 跨阶段必知事实（环境 / 路径 / 账号位置 / 工具 / 结论 / 坑）→ 影响 HANDOVER
- 外部对标 / 外部系统 / 来源地址 → 影响 REFERENCES

## annex 文件名前缀

按内容选前缀（**不是** pytest，**不是** 评测黄金集）：

| 前缀 | 何时 | 例 |
| --- | --- | --- |
| `VERIFY-` | 交付验收：改了什么、跑过什么 | `VERIFY-20260828-milvus-bm25.md` |
| `NOTE-` | REFERENCES 研究正文 | `NOTE-20260828-zimage-preset.md` |
| `CHECKLIST-` | 给人走的手工步骤 | `CHECKLIST-20260828-seed-l1.md` |
| `INDEX-` | **一天多件事**的当日索引：一行一事 + 指针，禁止贴正文 | `INDEX-20260828.md`（模板 `_INDEX.md`） |

取证进 `_raw/`（`.gitignore` 用 `templates/gitignore-memory.txt` 追加）。一天一事不建 INDEX。里程碑后旧 VERIFY / INDEX 进 `annex/_archive/`。

## 改 kit 本身（同步）

**权威源在远端仓库，不在本机。**

```text
https://github.com/RedOctupus/ai-agent-config-live
  └── materials/agent-skills/claude/project-memory-kit/    ← Claude Code 副本
  └── materials/agent-skills/cursor/project-memory-kit/    ← Cursor 副本
```

> 路径含 `materials/` 前缀：本仓库做过目录三分（`scaffold/` · `memory/` · `materials/`），kit 落在 `materials/` 下。按 `agent-skills/...` 找会落空。

改动流程：改任一副本 → push 到该仓库 → 另一份同步 → **`diff -r` 校验逐字一致**。
（两份分叉过一次，别再让它发生。）

**升版规则：** 动了 `templates/` / `references/` / `scripts/` 的可观察行为就改本文件顶部的 `kit v…`：
补句 / 修错字 → 末位 +1（`1.4.0` → `1.4.1`）；新增模板、字段或改设计门闸 → 中位 +1（→ `1.6.0`）。
项目侧靠 `MEMORY.md` §5 记的版本号判断该不该跟版。

**判定「补句」还是「改口令」——看改完之后，照文档干活的 Agent 会不会多做 / 少做 / 换个做法：**

- 只是让两处对**同一条既有口令**的表述对齐（其中一处本来就写全了）→ **补句**，末位 +1。
- 让 Agent 真的**多刷一个字段、多写一份文件、换掉 init 拷贝目标** → **改口令**，中位 +1。

拿不准时**按「改口令」高报**：高报只让人白跑一遍 `migration.md`，低报会让人跳过真要做的动作——JinRong 停版就是低报的后果。

本机这两处是由远端拷贝来的**安装位置，不是源**：

```text
%USERPROFILE%\.claude\skills\project-memory-kit\
%USERPROFILE%\.cursor\skills\project-memory-kit\
```

同步范围：`SKILL.md`、`README.md`、`templates/`、`references/`、`scripts/`；排除 `_sandbox/`。

## 明确不做

- 不把 Agent/用户行事哲学全文拷进项目
- 不默认生成支付、权限、部署模块
- 不把某个课程作业的 schema 写进通用 MEMORY 正文
