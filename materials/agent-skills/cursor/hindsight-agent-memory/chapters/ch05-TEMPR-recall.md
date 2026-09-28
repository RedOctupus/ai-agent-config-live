# Chapter 5: TEMPR Recall — Agent-Optimized Retrieval Architecture

## Core Idea
Recall 抛弃固定 top-k 接口，改成「调用方指定 token 预算 k」：四路并行检索 → RRF 融合 → cross-encoder 重排 → 按预算贪心装箱，让 agent 自己决定这次要多少记忆、花多少力气找。

## Frameworks Introduced
- **Token-budget 检索接口**（§4.2.1）: `Recall(B, Q, k)` 返回满足 Σ|fi| ≤ k 的事实集合，可选再加成本/延迟预算限制搜索扩展力度。
  - When to use: 下游是 LLM 而不是搜索页面时——返回的是「要塞进上下文的 token」，不是「要展示的条数」。
  - How: 简单问题给小 k「刚好够用」，多跳难题给大 k 换覆盖面。
- **四路并行检索（four-way parallel retrieval）**（§4.2.2）:
  1. **Semantic 语义通道**: query 嵌入 vQ 与记忆嵌入余弦相似，HNSW 索引的 pgvector 做 top-k——抓概念相似和改写表达。
  2. **Keyword 关键词通道**: 对记忆文本的 GIN 索引跑 BM25 全文检索——精确匹配专名、技术术语、数据集标识。
  3. **Graph 图通道（spreading activation 扩散激活）**: 以语义 top 命中为入口做 BFS，激活沿边传播 A(f,t+1) ∝ δ·A·…，δ ∈ (0,1) 衰减，边型乘子 μ(ℓ)：causal 和 entity 边 μ>1，弱语义/长程时间边 μ≤1——捞出文本不相似但共享实体/因果链的记忆。
  4. **Temporal 时间通道**: 查询检出时间约束时启动——先用两个开源日期解析库做规则归一化（'yesterday'、'June 2024' → 日期区间），解析不了的表达式回退到 seq2seq 模型 google/flan-t5-small 转成 [τstart, τend]；再用发生区间匹配 + 中点距离打分，图遍历被限制在命中集合 Rtemp 内。
- **RRF 重等排序融合（Reciprocal Rank Fusion）**（§4.2.3）: fused(f) = Σ_i 1/(k + ri(f))，k 为小常数（如 60），ri 是 f 在第 i 路列表的名次，缺席则该项为 0。
  - 为何不用分数融合: 基于名次就不需要各通道分数跨系统校准；缺失项不惩罚只贡献零；多路都靠前的条目自然浮顶（多证据支撑）。
- **Cross-encoder 重排**（§4.2.4）: RRF 后用 cross-encoder/ms-marco-MiniLM-L-6-v2 联合编码 query 与候选打相关分 CE(Q,f)——能建模 query-文档交互（而非独立向量），输入里还拼了格式化的时间信息让重排器利用时间线索。
- **Token 预算过滤**（§4.2.5）: 从重排列表头部顺序累加各条 token 数，加到 k 即止——贪心装箱，保证不超上下文容量。

## Key Concepts
- **Calibration-free fusion（免校准融合）**: RRF 只看名次，规避了向量分、BM25 分、激活值量纲不可比的问题。
- **Hybrid temporal parser（混合时间解析器）**: 规则解析覆盖多数查询（低延迟），seq2seq 兜底剩余——准确率与延迟的分层设计。
- **Configurable neural backbones（可配置神经骨干）**: 嵌入模型、重排器、生成 LLM 全是配置项。

## Mental Models
- 把四路通道想成四个各带偏见的证人：一个认意思（semantic）、一个认字面（BM25）、一个认关系（graph）、一个认时间（temporal）；RRF 是不看证词强度、只看排名的陪审团规则。
- 把 token 预算想成行李箱容量：重排决定优先级，装箱只管按序塞满即止——检索质量与上下文约束解耦。

## Reference Tables
| 通道 | 索引/技术 | 补什么盲区 |
|---|---|---|
| Semantic | HNSW + pgvector 余弦 | 改写、同义、跨表述 |
| Keyword | GIN + BM25 | 专名、术语的精确匹配 |
| Graph | BFS 扩散激活 | 共享实体/因果的间接关联 |
| Temporal | 规则日期解析 + flan-t5-small | 「什么时候」类查询 |

## Anti-patterns
- **固定 top-k 接口**: 条数相同 token 量可差数倍，且不随任务难度调整覆盖面。
- **单通道检索**: 只用向量会漏掉精确专名和实体链邻居——LongMemEval 多会话题正是这类。
- **分数直接加权融合**: 各通道量纲不同，权重调参脆弱；RRF 用名次绕开。
- **时间查询靠向量碰运气**: 时间表达必须显式解析成区间再匹配发生区间。

## Key Takeaways
1. 接口返回「预算内的事实集合」而不是 top-k——这是面向 LLM 的检索与面向人眼的检索的根本差别。
2. RRF (k≈60) 之后必须再做一次 cross-encoder 重排：融合给多样性，重排给精度。
3. 图通道靠 μ(ℓ) 把 causal/entity 边加权，是「间接相关」能被召回的机制所在。
4. 时间解析走规则优先、小模型兜底，两条路都失败才丢弃时间约束。

## Connects To
- **Ch 4**: 图通道遍历的正是 retain 建好的四类边
- **Ch 3**: 本章是 Recall(B,Q,k)→{f…} 的实现
- **Ch 7**: 作为 reflect 流水线第 1 步被调用
- **Ch 8**: 四路检索 + RRF + 重排是多会话/时间题大幅提升的直接原因
