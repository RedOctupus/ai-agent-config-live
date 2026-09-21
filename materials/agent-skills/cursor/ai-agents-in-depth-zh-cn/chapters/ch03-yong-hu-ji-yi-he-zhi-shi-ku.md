# Chapter 3: 用户记忆和知识库

## Core Idea
Agent 在单次对话结束后仍然需要“记住”用户和知识。用户记忆（User Memory）是个体尺度的持久化个性化模型，知识库（Knowledge Base）是群体尺度的共享领域知识。两者共用底层检索技术，但面向不同问题：前者让 Agent 成为“懂你的助手”，后者让 Agent 成为“领域专家”。

## Frameworks Introduced

- **用户记忆 vs 知识库**：同一问题的两个尺度。个体尺度关注用户偏好、习惯、身份；群体尺度关注行业法规、公司流程、专业文档。
- **记忆不是存储原始对话**：而是通过专门的 LLM 调用主动分析、抽象、结构化地提取对未来有用的事实。
- **记忆能力三层次评估框架**：
  1. 基础回忆：准确存储和检索用户直接提供的结构化信息
  2. 多会话检索：跨多个会话/对象/时期检索相关信息并推理
  3. 复杂联合推理：基于多个记忆片段联合思考、处理冲突、时间感知
- **四种用户记忆存储格式**：原始对话、摘要、结构化卡片、可执行代码/参数化记忆。
- **认知类型三分法**：情景记忆（episodic）、语义记忆（semantic）、程序记忆（procedural）。
- **记忆框架案例**：Mem0、Memobase 等开源/商业记忆系统的设计思路。
- **RAG 基础管道**：文档分块（Chunking）→ 嵌入（Embedding）→ 检索（Retrieval）→ 重排序（Rerank）→ 生成。
- **稠密嵌入 vs 稀疏嵌入**：稠密捕捉语义，稀疏捕捉精确关键词；混合检索兼顾两者。
- **结构化索引**：RAPTOR（递归摘要树）、GraphRAG（图结构知识）等超越扁平文本的知识组织方式。
- **文件系统范式**：用目录结构组织知识，让 Agent 通过文件路径和结构理解知识关系。
- **智能体化 RAG（Agentic RAG）**：把知识检索工具化，Agent 主动决定何时查、查什么、如何综合。
- **上下文感知检索**：根据当前任务和上下文动态选择检索策略和来源。
- **双层记忆架构**：Advanced JSON Cards（常驻概览）+ 上下文感知检索（按需取细节）。
- **隐私保护**：日志脱敏、隐私分级、最小权限原则。

## Key Concepts

- **User Memory**：用户记忆，跨会话保留的个性化信息。
- **Knowledge Base**：知识库，共享的领域知识集合。
- **RAG（Retrieval-Augmented Generation）**：检索增强生成，把外部知识注入上下文。
- **Chunking**：文档分块，平衡粒度、语义完整性与上下文长度。
- **Embedding**：嵌入，将文本映射到向量空间以支持语义检索。
- **Dense / Sparse Embedding**：稠密/稀疏嵌入，分别对应语义匹配和关键词匹配。
- **Hybrid Retrieval**：混合检索，结合多种检索方式提升召回率和精确率。
- **RAPTOR**：Recursive Abstractive Processing for Tree-Organized Retrieval，递归树形检索。
- **GraphRAG**：基于图结构的知识表示与检索。
- **Mem0 / Memobase**：代表性用户记忆框架。
- **Agentic RAG**：由 Agent 主动驱动的知识检索范式。
- **Context-aware Retrieval**：根据当前上下文动态调整检索策略。
- **Privacy-aware Logging**：隐私感知的日志与记忆处理。

## Mental Models

- **Memory is a predictive model**：用户记忆的目标不是记录，而是构建一个能预测用户需求的简洁模型。
- **Selective > exhaustive**：记住对未来有用的，忘掉临时细节。
- **Structured > raw**：结构化记忆便于检索、更新和冲突处理。
- **Retrieval is not just search**：RAG 的本质是“在正确的时间把正确的知识放到正确的上下文中”。
- **Knowledge needs governance**：知识库需要时效管理、版本控制和冲突解决机制。
- **Isolation + retrieval over compression**：与其压缩海量记忆，不如分层存储 + 按需检索。

## Anti-patterns

- **记住一切**：把每轮对话原始内容都存下来，导致噪声大、检索差。
- **忽视记忆冲突**：用户提供新信息时不更新旧记忆，导致前后矛盾。
- **知识过期不更新**：知识库一旦建立就不再维护，答案逐渐过时。
- **隐私泄露**：把敏感信息明文存储或不当使用。
- **检索召回不足**：分块过小、嵌入模型不匹配、缺少重排序。
- **把 RAG 当万能药**：RAG 解决的是“知识缺失”，不是“推理能力缺失”。

## Code Examples

```text
// 对话记忆提取示例：订票场景
User: Help me book a flight to Tokyo next Friday. I prefer window seats and I'm vegetarian.
User: Yes, and use my United MileagePlus number 12345678.

Extracted memories:
- User prefers window seats (preference)
- User is vegetarian, needs special meals (dietary restriction)
- User's United MileagePlus number: 12345678 (loyalty program)
- User has travel plans to Tokyo (recent activity)
```
- **What it demonstrates**：记忆提取是选择性的、抽象化的、结构化的，只保留对未来有用的事实，而非原始对话。

## Worked Example

**场景：跨会话的素食偏好与会员号记忆**

第一次订票时，用户提到自己是素食者并提供会员号。Agent 将这两条信息写入长期记忆：
- `dietary_restriction: vegetarian, special_meal_required`
- `loyalty_program: United MileagePlus 12345678`

两个月后用户再次说“帮我订去新加坡的航班”。Agent 检索记忆，无需再问：
- 自动筛选含素食餐食的航班
- 在结账时自动填入 MileagePlus 号码
- 只在座位偏好发生变化时确认

这就是“懂你的助手”——不是每次从零开始对话，而是基于持久化模型主动服务。

## Key Takeaways

1. **用户记忆和知识库是同一问题的两个尺度**：个体 vs 群体，共享底层检索技术但目标不同。
2. **好记忆 = 选择性 + 抽象化 + 结构化**：不是记录一切，而是提取对未来有用的事实。
3. **记忆能力分三层**：基础回忆 → 多会话检索 → 复杂联合推理，逐层递进。
4. **RAG 是知识注入的核心机制**：分块、嵌入、检索、重排序、生成，每一步都影响最终质量。
5. **混合检索 + 结构化索引优于纯向量检索**：关键词精确匹配、语义匹配、图/树结构各有适用场景。
6. **Agentic RAG 是趋势**：让 Agent 主动决定何时检索、如何综合，而不是被动拼接片段。
7. **隐私和时效是生产级记忆系统的两大底线**：脱敏、分级、更新机制缺一不可。

## Connects To

- **Ch 2 上下文工程**：用户记忆和知识库是上下文中“长期信息”的扩展。
- **Ch 4 工具**：检索工具、文件系统工具是记忆和知识库系统的实现依赖。
- **Ch 8 Agent 的持续进化**：Agent 如何根据使用经验更新记忆和知识库。
- **Ch 10 多 Agent 协作**：多 Agent 系统中的共享记忆与隐私隔离。
