# 业务上下文优先的 Agent 设计体系

## 状态

- 设计日期：2026-09-27
- 状态：用户已确认设计方向，进入实现
- 目标仓库：`D:\杂货铺\新建文件夹\ai-agent-config-live`

## 1. 背景与问题

当用户提出“新增一个 Agent”“给主管增加一个模块”“增加周报功能”时，Agent 很容易直接进入 prompt、工具、接口或页面设计，跳过业务域、业务生命周期、角色任务和任务上下文。这样会产生三类结构性问题：

1. 把角色误当成 Agent 边界，例如“主管 Agent”“安全管理员 Agent”；
2. 把原子动作误当成 Agent，例如“查询 Agent”“编写 Agent”；
3. 只实现生命周期前半段或单个页面，没有明确上下游、跨域依赖、记忆和人工责任。

项目需要一套跨项目可复用的流程，提醒人和 Agent 在开发前先完成业务上下文分析，同时不把每个小修复都升级成完整领域建模。

## 2. 目标

### 必须实现

- 提供独立技能 `business-context-first-agent-design`。
- 对新增 Agent、能力模块、角色视图、多 Agent 协作、记忆读写和跨域流程提供业务上下文优先的设计流程。
- 按 L0–L3 判断分析深度：L0 局部修复、L1 已有场景扩展、L2 新 Agent/能力模块、L3 跨域/多 Agent/平台级变化。
- 在 L2/L3 任务中检查业务域、生命周期、角色任务、上下文、Agent 结果边界、原子能力、能力模块、角色视图、记忆和人工确认。
- 允许在没有 project-memory-kit 的项目中以兼容模式创建最小的 `docs/agent-context/` 槽位。
- 在已经使用 project-memory-kit 的项目中优先使用 `docs/memory/BUSINESS-CONTEXT.md`，并把详细内容分别沉淀到 REQUIREMENTS / FLOW / FRAMEWORK / TODO / ITERATION。
- 为 kit 提供 `BUSINESS-CONTEXT.md` 模板和显式路由规则。
- 同步 Claude、Cursor 和 portable 三份通用 Skill；同步 Claude/Cursor 两份 project-memory-kit 副本。

### 不做

- 不把 Skill 变成完整项目管理系统。
- 不为每个角色创建一个 Agent。
- 不强制普通 bug 修复执行完整业务域分析。
- 不复制一套与 project-memory-kit 平行的完整记忆目录。
- 不引入新的运行时依赖。
- 不把任何具体行业 schema 写入通用 Skill 或 Kit。
- 不使用 DeepEval 作为 Skill 正确性的唯一判断；本次优先使用可复现的压力场景和结构检查，若模型评测需要再单独接入。

## 3. 核心模型

```text
宏观项目业务流
  → 业务域
  → 业务域生命周期
  → 角色任务场景
  → 任务上下文
  → Agent 协作
  → 原子能力
  → 能力模块
  → 角色视图
  → 跨域编排与状态回流
```

- 角色：调用者、责任人、权限和客户端视图的来源，不直接等于 Agent。
- Agent：对稳定业务结果负责的协作单元；命名按职责/结果，不按角色，不按单一工具动作。
- 原子能力：可复用、输入输出清晰、可独立测试的查询、检索、比较、生成、校验、记忆读写等动作。
- 能力模块：围绕业务结果和生命周期闭环封装的一组 Agent、原子能力、上下文、记忆策略和人工边界。
- `BUSINESS-CONTEXT.md`：业务上下文地图、索引和开发前门闸，不复制各源文件正文。

## 4. 两个组件的联动

### 4.1 project-memory-kit

Kit 是项目级路由器和长期存储协议：

- 维护触发规则、文件落点和变更同步纪律；
- 初始化或识别 `docs/memory/BUSINESS-CONTEXT.md`；
- 规定角色任务写入 REQUIREMENTS，生命周期/编排写入 FLOW，Agent/能力模块写入 FRAMEWORK，行动型缺口写入 TODO，决策原因写入 ITERATION；
- 在项目规则中要求涉及 Agent 设计时加载独立 Skill。

### 4.2 business-context-first-agent-design

独立 Skill 是条件触发的分析方法：

- 在任务开始时做 L0–L3 分级；
- 按级别运行业务域、生命周期、角色任务、上下文和 Agent 边界检查；
- Kit 存在时写入既有 `docs/memory/` 体系；
- Kit 不存在时，在不覆盖既有文档的前提下初始化 `docs/agent-context/` 最小兼容槽位；
- 输出“可进入实现 / 受控原型 / 先补上下文”的结论。

Kit 不通过代码动态调用 Skill；它通过 AGENTS/MEMORY/Cursor 规则提供确定性路由，Skill 通过自身 description 支持无 Kit 项目的发现。

## 5. 文件设计

### 独立 Skill

```text
materials/agent-skills/portable/business-context-first-agent-design/
├── SKILL.md
└── references/
    ├── lifecycle-analysis.md
    ├── context-inventory.md
    ├── agent-boundary.md
    └── review-gates.md
```

Claude 和 Cursor 下保留同内容副本，便于按现有备份规则恢复。

### Kit 新增

```text
materials/agent-skills/{claude,cursor}/project-memory-kit/
└── templates/BUSINESS-CONTEXT.md
```

不增加 parallel `agent-design/` 记忆树。

### 项目实例

有 Kit：

```text
docs/memory/BUSINESS-CONTEXT.md
```

无 Kit：

```text
docs/agent-context/
├── BUSINESS-CONTEXT.md
├── AGENT-DESIGN.md
└── OPEN-QUESTIONS.md
```

## 6. Skill 流程

1. 读取项目入口文件，确认是否有 Kit、现有业务文档和当前工作区状态。
2. 判断任务级别：L0/L1/L2/L3。
3. L0 只做局部变更；L1 读取相关既有上下文；L2/L3 建立或补齐业务上下文。
4. 定位业务域和业务域生命周期，标记本任务所在节点、前置条件和后续状态。
5. 识别角色、角色任务、触发条件、预期结果和人工责任。
6. 盘点业务、对象、时间、规则、记忆、权限和证据上下文，并区分已知/模拟/未知/待确认。
7. 按业务结果拆 Agent；拒绝 Role-as-Agent 和 Tool-as-Agent。
8. 定义 Agent 输入、输出、记忆读写、人工边界、失败处理和协作关系。
9. 拆出可复用原子能力，封装成能力模块。
10. 映射到角色视图，并回到宏观业务流检查跨域影响和状态回流。
11. 检查是否达到 GREEN/YELLOW/RED：可实现、可做受控原型、必须先补上下文。
12. 将结果写入 Kit 槽位或 standalone 兼容槽位；实现后再更新记忆和验证记录。

## 7. Kit 槽位映射

| 业务上下文内容 | 正式落点 |
|---|---|
| 索引、状态、缺口总览 | `BUSINESS-CONTEXT.md` |
| 角色任务、故事、验收 | `REQUIREMENTS.md` |
| 域生命周期、端到端编排、跨域流程 | `FLOW.md` |
| 能力模块、Agent、原子能力、分层 | `FRAMEWORK.md` |
| 可执行的上下文补齐动作 | `TODO.md` |
| 设计决策和原因 | `ITERATION.md` |
| 当前阶段一句话 | `MEMORY.md` |

## 8. 兼容模式

无 Kit 时，Skill 只在 L2/L3 或用户明确要求初始化时创建 `docs/agent-context/`。已有 `docs/`、`requirements/`、`architecture/`、`workflows/`、`agents/` 时先复用和建立指针，不覆盖或复制正文。后续安装 Kit 时按映射迁移，不静默覆盖。

## 9. 验证策略

- RED：用六个压力场景测试无 Skill 基线，记录模型直接 Agent-first/UI-first 的行为。
- GREEN：用同一六个场景测试 Skill 文本、Kit 路由和模板结构；至少验证 L0 不被过度流程化，L2/L3 能拦截直接实现。
- REFACTOR：检查 Skill 是否重复、过长、把所有任务都升级为 L3，或只会列问题而不给下一步。
- 仓库验证：模板双副本一致、三份 Skill 一致、YAML frontmatter 合法、脚本/文档检查通过、项目 Kit 体量门闸通过。
- DeepEval 非必需：只有当有稳定的模型调用入口、数据集和可复现指标时才引入；本次使用 DeepSeek 压力场景和结构化评分即可。
