# Chapter 10: 多 Agent 协作

## Core Idea
单个 Agent 受限于模型能力边界和上下文窗口。多 Agent 协作不只是让不同专长的 Agent “取长补短”，更可能涌现出 **群体智能**——多个专家级 Agent 组织得当，整体能力可能超过个体简单相加。本章围绕两个核心设计维度展开：上下文是否共享，以及 Agent 之间如何协调。

## Frameworks Introduced

- **AI 能力五等级**：Level 1 对话者 → Level 2 思考者 → Level 3 智能体 → Level 4 创新者 → Level 5 组织。多 Agent 协作常被类比为通向第五级的路径之一。
- **多 Agent 协作的两个核心设计维度**：
  1. **上下文是否共享**：继承式协作（共享上下文） vs 隔离式协作（独立上下文 + 显式通信）
  2. **协调模式**：串行、并行、协商、竞争、市场机制等
- **共享上下文（继承式协作）**：后一 Agent 继承前一 Agent 的完整对话历史和轨迹，切换系统提示词和工具集后变成新角色。优势是信息不丢失；挑战是上下文快速膨胀。
- **不共享上下文（隔离式协作）**：每个 Agent 维护独立上下文，通过显式通信机制交换信息。优势是模块化和隔离性好；挑战是需要设计清晰的接口和通信协议。
- **Agent 间通信的 IPC 两大范式**：
  - 共享内存：共享文件系统（适合大产物、持久化）
  - 消息传递：工具调用参数（同步、结构化）和消息总线（异步、解耦）
- **“不要通过共享内存通信，而要通过通信共享内存”**：共享内存快但易冲突；消息传递清晰但需编排。
- **消息总线（Message Bus）**：专门负责 Agent 间消息中转的异步通信机制，适合并行协调。
- **并行协调**：多个 Agent 并行工作，消息总线协调依赖关系。
- **角色化分解**：按需求分析师、软件工程师、代码审查员等角色拆分任务，每个 Agent 专注特定职责。
- **冲突与共识**：多 Agent 系统中需要处理意见冲突、达成共识、终止无意义争论。
- **人类介入点**：在关键决策点引入人类确认或仲裁。
- **多 Agent 系统的可观测性**：追踪跨 Agent 消息流、状态变化、决策链路。

## Key Concepts

- **Multi-Agent System**：多 Agent 系统。
- **Collective Intelligence**：群体智能，多个 Agent 协同涌现出的超越个体的能力。
- **Shared Context**：共享上下文，Agent 继承前任的完整对话历史。
- **Isolated Context**：隔离上下文，Agent 只通过显式通信共享信息。
- **Shared File System**：共享文件系统，作为 Agent 间“共享内存”。
- **Message Bus**：消息总线，异步中转 Agent 间消息。
- **Tool Parameter Passing**：工具调用参数传递，同步结构化通信。
- **IPC（Inter-Process Communication）**：进程间通信，共享内存 vs 消息传递。
- **Role-based Decomposition**：基于角色的任务分解。
- **Coordination Pattern**：协调模式（串行、并行、协商、竞争、市场）。
- **Consensus**：共识机制，多 Agent 达成一致。
- **Conflict Resolution**：冲突解决机制。
- **Human-in-the-loop**：人类在关键决策点介入。

## Mental Models

- **More agents ≠ better**：组织方式比数量更重要。
- **Isolation is the default**：除非有明确理由，否则优先隔离上下文，通过显式通信协作。
- **Shared context is a memory leak risk**：完整共享上下文会导致快速膨胀和隐私问题。
- **Message bus = email system for agents**：异步、解耦、适合并行协调。
- **Shared filesystem = shared memory for agents**：适合大产物和持久化，但要注意并发冲突。
- **Specialization + coordination = emergence**：专业分工 + 有效协调 = 群体智能。
- **Design interfaces, not just agents**：多 Agent 系统的关键设计是 Agent 之间的接口和协议。

## Anti-patterns

- **无差别共享上下文**：所有 Agent 都看到所有信息，导致上下文膨胀和隐私泄露。
- **缺少清晰接口**：Agent 之间职责边界模糊，互相推诿或重复工作。
- **同步串行所有任务**：白白浪费并行机会。
- **没有冲突解决机制**：多 Agent 意见不一致时系统死锁。
- **忽视人类介入点**：关键决策完全由 Agent 自主，缺乏人类监督。
- **过度协调开销**：协调成本超过并行收益。
- **把多 Agent 当万能解**：很多任务单个 Agent 就能做好，不要为了多 Agent 而多 Agent。

## Code Examples

```text
// 隔离式协作：翻译流水线

阶段1：Glossary Agent
sys: "识别术语并翻译..."
tools: [search_dict, write_file]
→ 输出 glossary.json

阶段2：Translation Agent
sys: "翻译本章内容，参考 glossary..."
tools: [read_file, write_file]
→ 输入 glossary.json
→ 输出 chapter1_zh.md

阶段3：Proofreading Agent
sys: "检查术语一致性..."
tools: [read_file, write_file]
→ 输入 glossary.json + chapter1_zh.md
→ 输出 review_report.md

// 通信机制：共享文件系统（共享内存）+ 消息总线（消息传递）
```
- **What it demonstrates**：隔离式协作中每个 Agent 职责清晰、上下文独立，通过共享文件系统传递产物，适合需要严格分工和可审计的流水线任务。

## Worked Example

**场景：软件需求 → 开发 → 审查的多 Agent 流水线**

1. **需求分析师 Agent**（共享上下文 / 继承式）：
   - 与用户充分沟通，确认需求
   - 输出：需求文档 + 与用户的沟通记录

2. **软件工程师 Agent**（切换角色，继承上下文）：
   - 根据需求编写代码
   - 输出：代码文件 + 测试脚本

3. **代码审查员 Agent**（切换角色，继承上下文）：
   - 运行 linter 和测试，审查代码
   - 输出：审查报告

**对比隔离式方案**：
- 如果每个 Agent 不共享上下文，则通过共享文件系统传递：需求文档、代码、测试脚本、审查报告。
- 隔离式更好：每个 Agent 只需关注自身上下文，模块化强，易于扩展和维护。
- 但信息可能在传递中丢失，需要设计好产物格式和元信息。

## Key Takeaways

1. **多 Agent 协作是突破单个 Agent 能力边界的关键工程手段**：解决上下文窗口、能力专精、可靠性问题。
2. **上下文共享 vs 隔离是首要架构决策**：共享上下文信息完整但易膨胀；隔离上下文模块化好但需显式通信。
3. **Agent 间通信落回 IPC 两大范式**：共享文件系统（共享内存）和消息传递（工具参数、消息总线）。
4. **消息总线适合异步并行协调**：解耦发送方和接收方，支持多个 Agent 并行工作。
5. **多 Agent 系统的关键设计是接口和协议**：不是 Agent 数量，而是如何分工和协作。
6. **冲突解决、共识、人类介入是多 Agent 系统可靠运行的必要机制**。
7. **不要为了多 Agent 而多 Agent**：简单任务单个 Agent 可能更好；多 Agent 的收益必须大于协调开销。

## Connects To

- **Ch 1 AI Agent 入门**：单个 Agent 的组成和循环是多 Agent 系统的基础。
- **Ch 2 上下文工程**：子 Agent 上下文隔离是上下文工程的高级应用。
- **Ch 4 工具**：协作工具、消息总线是多 Agent 系统的通信基础设施。
- **Ch 5 Coding Agent**：Coding Agent 可作为子 Agent 被主 Agent 委托任务。
- **Ch 8 Agent 的持续进化**：多 Agent 系统的协作经验可沉淀为新的协作模式或 Skill。
- **Ch 9 多模态与实时交互**：多 Agent 实时协调需要消息总线和异步机制。
