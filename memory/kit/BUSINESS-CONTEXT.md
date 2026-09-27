# 业务上下文索引

> 本仓不是业务应用；本文件用于记录本次“业务上下文优先 Agent 设计”能力本身的设计上下文，验证 Kit 的可选槽位。具体方法正文在 `materials/agent-skills/`，Kit 规则在对应 `project-memory-kit/SKILL.md`。

## 0. 分析状态

- 当前任务：新增通用业务上下文优先 Agent 设计 Skill，并接入 project-memory-kit
- 任务级别：L3（跨运行时技能、Kit 路由、模板、沙盒验证）
- 当前阶段：已实现，已本地提交，待远端同步
- 决策：GREEN
- 是否允许进入代码：是
- 阻塞项：无

## 1. 项目级业务流

```text
用户提出复杂 Agent / 能力模块需求
→ Kit / 项目入口识别任务级别
→ 设计 Skill 补齐业务域与生命周期上下文
→ 结果落到需求 / 流程 / 框架 / 缺口记录
→ 进入实现与验证
→ 更新 Skill / Kit 记忆与 VERIFY
```

## 2. 业务域

| 业务域 | 是否涉及 | 范围 | 状态 | 详情 |
|---|---:|---|---|---|
| Agent 设计流程 | 是 | 跨项目通用方法 | 已定 | `materials/agent-skills/*/business-context-first-agent-design/` |
| 项目记忆 Kit | 是 | 路由、模板、落点 | 已定 | `materials/agent-skills/{claude,cursor}/project-memory-kit/` |

## 3. 业务域生命周期

| 业务域 | 生命周期 | 当前节点 | 前置条件 | 产生的状态 / 下游 |
|---|---|---|---|---|
| Agent 设计流程 | 需求 → 分析 → 设计 → 实现 → 验证 → 记忆同步 | 验证 / 收口 | Skill、Kit 模板、压力场景 | 可复用 Skill + kit v1.4.0 |

## 4. 角色任务场景

| 角色 | 任务 | 触发条件 | 预期业务结果 | 人工责任 | 详情 |
|---|---|---|---|---|---|
| Agent 开发者 | 新增 Agent 或能力模块前补齐业务上下文 | 用户提出 L2/L3 任务 | 避免 Agent-first，形成可评审设计 | 确认业务边界和 YELLOW 假设 | 独立 Skill |
| 项目记忆维护者 | 将分析结果落到 Kit 槽位 | 业务设计完成或变更 | 需求 / 流程 / 框架 / 缺口可追溯 | 决定是否升级 Kit 版本 | project-memory-kit |

## 5. 上下文清单

### 已知上下文

- 目标仓库：本仓 `ai-agent-config-live`
- 交付形态：portable、Claude、Cursor 三份 Skill；Claude/Cursor 两份 Kit
- 共享协议：`BUSINESS-CONTEXT.md`
- 验证：DeepSeek 六场景基线与有指导复测、artifact checks、memory size gate

### 模拟上下文

- 无业务应用数据；本仓以技能和记忆文档为业务设计载体

### 未知或待确认上下文

- 不同宿主对 Skill 自动发现的具体优先级可能不同；已用 Kit 规则 + Skill description 双重路由降低风险

### 必须人工确认的上下文

- Skill 是否被正式安装 / 启用：本仓只备份，不自动注册本机技能

## 6. Agent 与原子能力

- 设计 Skill 不是项目运行时 Agent；其业务结果是引导开发者完成上下文优先设计。
- 关键原子能力：任务分级、业务域定位、生命周期定位、上下文盘点、Agent 边界检查、能力模块封装、视图映射、门闸判定。

## 7. 能力模块

| 能力模块 | 覆盖业务域 | 覆盖生命周期 | 参与 Agent | 消费角色视图 | 状态 |
|---|---|---|---|---|---|
| 业务上下文优先 Agent 设计 | Agent 设计流程 | 需求到验证 | 设计 Skill + Kit 路由 | Agent 开发工作流 | 已实现 |

## 8. 角色视图映射

| 角色视图 | 可见结果 | 可调用能力 | 可执行动作 | 只读 / 模拟限制 |
|---|---|---|---|---|
| 开发者工作流 | GREEN / YELLOW / RED、上下文缺口、设计落点 | Skill、Kit 模板、项目记忆 | 补上下文、设计、实现、验证 | 本仓不自动安装或注册技能 |

## 9. 跨域协作

- Kit 负责项目级路由和长期落点；设计 Skill 负责分析方法；`BUSINESS-CONTEXT.md` 负责共享索引。
- 有 Kit 时写入 `docs/memory/`；无 Kit 时由 Skill 使用 `docs/agent-context/` 兼容模式。
- 完成后更新 `REQUIREMENTS / FLOW / FRAMEWORK / ITERATION / annex VERIFY`。

## 10. 上下文缺口

| 缺口 | 影响 | 处理方式（询问 / 模拟 / 延后 / 停止） | 是否阻塞 |
|---|---|---|---|
| 宿主 Skill 自动发现差异 | 可能只靠 description 触发 | Kit 规则 + Skill description 双重路由 | 否 |

## 11. 开发前门闸

- [x] 业务域明确并有边界
- [x] 生命周期和当前节点明确
- [x] 角色任务和业务结果明确
- [x] 上下文已盘点并标记已知 / 模拟 / 未知 / 假设 / 人工确认
- [x] Agent / Skill 不按角色命名
- [x] 原子能力与职责边界明确
- [x] 能力模块和生命周期覆盖范围明确
- [x] 角色视图已映射
- [x] 跨域影响和状态回流已检查
- [x] 人工确认点已明确
- [x] 未知内容没有被静默编造
