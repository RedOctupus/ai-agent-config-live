# Chapter 4: TEMPR Retain — Building a Temporal-Entity Memory Graph

## Core Idea
Retain 不是把对话切成句子存向量，而是用 LLM 抽出「自包含的叙事事实」，连同时间区间、实体和四类图链接一起写进记忆图——存储粒度决定了下游检索能否跨轮次还原上下文。

## Frameworks Introduced
- **记忆单元元组（memory unit tuple）**（§4.1.1）: 每条记忆 = (u, b, t, v, τs, τe, τm, ℓ, c, x)——u 唯一 ID、b 库 ID、t 叙事文本、v ∈ R^d 嵌入向量、τs/τe 发生区间、τm 提及时间、ℓ 事实类型、c ∈ [0,1] 可选置信度（仅 opinion）、x 辅助元数据（上下文、访问次数、全文检索向量）。一条事实只入一张网络，由 ℓ(f) ∈ {world, experience, opinion, observation} 决定。
  - When to use: 设计任何「一条记忆既要做向量检索、又要做词法/时间/信念查询」的存储。
- **叙事事实抽取（narrative fact extraction）**（§4.1.2）: 粗粒度分块，每次对话抽 2–5 条综合事实，每条覆盖整个交互而非单句。
  - How: 事实要叙述完整、自包含、包含全部参与者、保留对话的语用流向（谁提议、谁反对、为何采纳）。
- **六步抽取流水线**（§4.1.2）: 1) 共指消解 2) 时间表达式归一化（'last week' → 绝对 τs,τe）3) 参与者归因（谁做了/说了什么）4) 保留显式推理与理由 5) 事实类型分类入网 6) 实体抽取（PERSON/ORGANIZATION/LOCATION/PRODUCT/CONCEPT/OTHER）。嵌入前再拼一条人类可读时间引用，提升时间召回与重排。
- **实体消解函数 ρ: M → E**（§4.1.3）: mention → canonical entity，按最大化相似度 sim = α·sim_str + β·sim_co + γ·sim_temp——字符串相似（Levenshtein）、共现模式、时间邻近三项加权。
- **四类图链接**（§4.1.4）: 每条边 e = (fi, fj, w, ℓ)，w ∈ [0,1]：
  - **temporal**: 时间接近的两条记忆相连，权重随 Δtij 增大按衰减参数 σt 衰减；
  - **semantic**: 余弦相似超阈值 θs 才连；
  - **entity**: 同一 canonical entity 的所有记忆两两双向连接；
  - **causal**: LLM 抽取的因果关系，权重固定 1.0，类型 ∈ {causes, caused_by, enables, prevents}，遍历时上调权重以偏爱解释性连接。
- **观察范式（observation paradigm）**（§4.1.5）: 对实体 e，从提及它的事实集合 Fe 用 LLM 摘要函数生成偏好中立画像 oe；新增事实时后台异步重算，保证低延迟写入。
  - **Observations vs Opinions 四点区别**: ① observation 不受行为画像影响，opinion 被画像参数调制；② observation 是中立摘要，opinion 是主观评价；③ observation 无置信度，opinion 有 c ∈ [0,1]；④ observation 靠背景合成、事实变了就重新生成，opinion 在 reflect 中形成、靠强化更新。

## Key Concepts
- **Coarse-grained chunking（粗粒度分块）**: 2–5 facts/次对话；让检索对局部切分决策不敏感。
- **Coreference resolution（共指消解）**: 'my roommate' 和 'Emily' 必须链成同一实体（附录 A.1 标为 CRITICAL）。
- **Background regeneration（后台重算）**: 观察生成/再生成异步执行，写路径低延迟、摘要质量随事实累积渐进变好。

## Mental Models
- 把叙事事实想成「迷你新闻稿」而不是「数据库行」：五个 W（what/when/where/who/why）齐全，检索到一条就能独立理解。
- 把记忆图想成给向量库加了一层「人工索引」：向量解决相似，图边解决「同一实体/同一时刻/因果」这三种向量算不出来的关联。

## Worked Example — Figure 3：碎片化 vs 叙事抽取
**碎片化（避免）**，存 5 条：'Bob suggested Summer Vibes' / 'Alice wanted something unique' / 'They considered Sunset Sessions' / 'Alice likes Beach Beats' / 'They chose Beach Beats'。
**叙事抽取（采用）**，存 1 条：「Alice and Bob discussed naming their summer party playlist. Bob suggested 'Summer Vibes' because it is catchy and seasonal, but Alice wanted something more unique. Bob then proposed 'Sunset Sessions' and 'Beach Beats,' with Alice favoring 'Beach Beats' for its playful and fun tone. They ultimately decided on 'Beach Beats' as the final name.」——保留了提议链、理由和最终决定，单条即可回答「谁定了歌单名、为什么」。

## Anti-patterns
- **句子级切分**: 五条碎片各自检索都「相关」，但没有一条能回答决策过程；推理对切分点过拟合。
- **mention 与 canonical 实体不合并**: 检索 'Emily' 时漏掉 'my roommate'，多跳链断掉。
- **observation 携带评价词**: 'John seems like a good person' 混入了推断——附录 A.3 明确列为反例。

## Key Takeaways
1. 存储粒度选叙事事实（2–5 条/对话），不选句子——跨轮上下文是回答长程问题的必要信息。
2. 每条记忆自带 (τs, τe, τm) 和嵌入向量，同一份数据同时支撑语义、词法、时间、信念四种查询。
3. 四类边里 causal 和 entity 权重最高，是图遍历能补向量检索盲区的原因。
4. observation 是「物化视图」，异步重算即可；opinion 是「有状态记录」，必须走强化机制。

## Connects To
- **Ch 3**: 本章是 Retain(B,D)→M′ 的实现
- **Ch 5**: 建好的图是 Recall 四路检索中图遍历通道的输入
- **Ch 6**: retain 完成后触发 opinion reinforcement 和 background merging
- **Ch 10**: 事实抽取提示词与 ExtractedFact schema 的原文
