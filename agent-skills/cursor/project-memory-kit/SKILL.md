---
name: project-memory-kit
description: >-
  Initializes and maintains compact project memory for humans and agents.
  Use when the user says init a new project, 初始化项目记忆, 新建项目脚手架,
  or when a repo already has docs/memory/ and the task changes requirements,
  requirement breakdown, architecture, TODOs, 服务对象大环境, 项目框架, 实现流程, or needs a test report.
---

# Project Memory Kit

人读 [README.md](README.md)。Agent 以本文件为准。

人机共用上下文：MEMORY 快照 + ENVIRONMENT / REQUIREMENTS / FRAMEWORK / FLOW 源文件 + 迭代 / TODO / 测试日志。行事哲学原文不拷进项目。

## 路径约定

Init 后新项目：

```text
docs/memory/MEMORY.md       # 各阶段一句话快照、约束、入口
docs/memory/ENVIRONMENT.md  # 服务对象大环境（现状）
docs/memory/REQUIREMENTS.md # 拆解条目，对照开发
docs/memory/FRAMEWORK.md    # 项目框架：选型、能力模块、分层
docs/memory/FLOW.md         # 实现流程：端到端怎么走
docs/memory/TODO.md
docs/memory/ITERATION.md
docs/memory/tests/YYYYMMDD-任务名.md
AGENTS.md
.cursor/rules/project-memory.mdc
```

本 Skill 目录：`templates/` 可拷贝；`references/` 不拷进项目，按需再读。

- 协作 / 模式选择：[references/collaboration.md](references/collaboration.md)
- 阅读、最小修改、测试汇报：[references/agent-rules.md](references/agent-rules.md)
- MVC 与工程骨架：[references/scaffold.md](references/scaffold.md)
- 存量项目收敛：[references/migration.md](references/migration.md)
- 多人 / 多模块维护：[references/team.md](references/team.md)

## 本 Skill 何时打开（不是日常阅读策略）

日常改代码**不会**读这份 SKILL。何时读 TODO / 测试日志 / 源文件 / `references/`：**以项目里 `MEMORY.md` 第 5 节为准。**

本 SKILL 只在这些时候打开（与 MEMORY 第 5 节「Skill references」一致）：

| 情况 | 读 |
| --- | --- |
| 用户说 init / 初始化项目记忆 | 本 SKILL + `templates/` |
| 大任务定型、Ask/Plan | [references/collaboration.md](references/collaboration.md) |
| 不确定改法、怎么验 | [references/agent-rules.md](references/agent-rules.md) |
| 用户点名工程脚手架 | [references/scaffold.md](references/scaffold.md) |
| 已有 memory 但不符合骨架（收敛） | [references/migration.md](references/migration.md) |
| 项目有多个维护者 / 多模块 | [references/team.md](references/team.md) |

## Init（用户说 init 新项目 / 初始化项目记忆）

目标目录：当前工作区根；若用户指定了路径，用用户路径。

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
| `templates/ITERATION.md` | `docs/memory/ITERATION.md` |
| `templates/tests/_TEMPLATE.md` | `docs/memory/tests/_TEMPLATE.md` |
| `scripts/check-memory-size.py` | `scripts/check-memory-size.py`（体量门闸；AGENTS.md / MEMORY 按**项目内相对路径**调用它，故须随 init 落地，否则那条命令在项目根直接失败） |
| `templates/AGENTS.md` | 项目根 `AGENTS.md`（已有则合并指针，不抹掉用户原文） |
| `templates/cursor-rule.mdc` | `.cursor/rules/project-memory.mdc` |

多模块 / 多人：走 [references/team.md](references/team.md)；根索引用 `templates/ROOT-MEMORY.md`、认领表用 `templates/OWNERS.md`，模块子目录复用上表单项目模板。

3. 只填 MEMORY 里立刻知道的项（文件夹名、当前阶段若用户已说）。其余留空，不编造业务。
4. **默认只 init 记忆目录 + 体量门闸脚本。** 仅当用户明确要工程脚手架时，再按 `references/scaffold.md` 生成 `.gitignore`、`.env.example`、`README.md` 骨架。不要默认生成 RBAC、JWT、Docker。
5. 向用户汇报创建了哪些路径。

## 日常维护（已 init）

不是 Cursor 出厂默认；依赖项目里的 `project-memory.mdc`。按任务规模更新：

| 事件 | 动作 |
| --- | --- |
| 大任务开始 | 对齐 `ENVIRONMENT.md`；需求写入 `REQUIREMENTS.md`；框架写入 `FRAMEWORK.md`（**每一项技术栈须用户确认后才能当作已定**）；实现流程写入 `FLOW.md`；MEMORY 只改对应一句话；再更新 `TODO.md`；**先跑 `python scripts/check-memory-size.py` 校验体量（超阈值先裁剪）并刷新 §0 HEAD** |
| 需求讨论定稿或条目增删 | 改 `REQUIREMENTS.md`；目的一句话变了才改 MEMORY 快照；追加 `ITERATION.md` |
| 选型或模块变更 | 先与用户确认该技术栈；再改 `FRAMEWORK.md`；骨架一句话变了才改 MEMORY 快照；追加 `ITERATION.md` |
| 实现流程变更 | 改 `FLOW.md`；链路一句话变了才改 MEMORY 快照；追加 `ITERATION.md` |
| 交付 / 验收相关改动 | 新建 `docs/memory/tests/YYYYMMDD-任务名.md`（用 `_TEMPLATE.md`） |
| 服务对象**真实办事方式**变了 | 才更新 `ENVIRONMENT.md`；大环境一句话变了才改 MEMORY 快照 |
| 项目里程碑 | 源文件若变了就改源文件；MEMORY 只改变了的那句快照；追加 `ITERATION.md`；**默认不改大环境** |
| 小改动 | 仅当状态变化时改 MEMORY/TODO；不强制写源文件或测试日志 |

更新 MEMORY 时：**只改快照一句话和约束/入口，禁止往里粘源文件正文。** 变更记录只追加 `ITERATION.md`。详见 MEMORY 模板「体量」节。

测试 / 验收：新建 `tests/YYYYMMDD-任务名.md` 写战报；逐轮结果、逐缺陷状态、复跑取证只进 `tests/`，**不进 MEMORY**；截图 / 原始 JSON / stdout 放 `tests/*/_raw/` 并 `.gitignore` 掉 `_raw/shots/`，只提交手写 `.md`。

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

## 测试日志文件名

`docs/memory/tests/YYYYMMDD-短任务名.md`，例如 `20260828-milvus-bm25.md`。

每个里程碑收口后，把旧的 TEST-LOG 挪到 `docs/memory/tests/_archive/`，MEMORY §0 只留最近里程碑的指针，避免 `tests/` 无限累积。

## 改 kit 本身（同步）

改本 Skill 源（课程治理框架里的 `project-memory-kit/`）后，必须 re-copy 到个人 skills 并 diff 校验，否则两套分叉：

```text
源 → %USERPROFILE%\.cursor\skills\project-memory-kit\   （Cursor）
源 → %USERPROFILE%\.claude\skills\project-memory-kit\    （Claude Code）
```

同步范围：`SKILL.md`、`README.md`、`templates/`、`references/`、`scripts/`；排除 `_sandbox/`。改完 `diff -r` 确认一致。

## 明确不做

- 不把 Agent/用户行事哲学全文拷进项目
- 不默认生成支付、权限、部署模块
- 不把某个课程作业的 schema 写进通用 MEMORY 正文
