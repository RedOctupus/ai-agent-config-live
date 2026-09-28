# Patterns

## Pattern 1: Narrative Fact Extraction（叙事事实抽取）
**When to use**: 把对话/文档写入记忆库的抽取阶段。
**How**: 粗粒度分块（2–5 条事实/对话）；每条覆盖整个交互，五维齐全（what/when/where/who/why，when 精确到星期）；先共指消解再归一时间；LLM 输出接 Pydantic 强校验。
**Trade-offs**: 存储粒度粗、单条较长，但检索对切分点不敏感，单条即可独立回答；碎片化抽取省 token 却丢推理链。

## Pattern 2: Four-Network Epistemic Partition（四网络认知分区）
**When to use**: 存储层需要区分「观察到的 / 自己经历的 / 合成的 / 相信的」。
**How**: 每条事实按 fact_type 只入一张网络；opinion 带 (t, c, τ)，observation 只从 W/B 合成且不带评价；抽取时分类。
**Trade-offs**: 写路径多一次分类，换来回答时可追溯与信念可演化。

## Pattern 3: Token-Budget Retrieval Interface（token 预算检索接口）
**When to use**: 检索结果直接喂 LLM 而非展示给人。
**How**: `Recall(B, Q, k)` 返回 Σ|fi| ≤ k；重排决定优先级，贪心装箱执行预算；可选成本/延迟预算封顶。
**Trade-offs**: 调用方需预估预算；换来上下文占用可控、难度自适应覆盖面。

## Pattern 4: Four-Way Parallel Recall + RRF（四路并行检索 + 名次融合）
**When to use**: 查询混合了语义、专名、关系、时间四类需求。
**How**: 语义(HNSW/pgvector)、关键词(GIN/BM25)、图(扩散激活)、时间(规则+flan-t5)四路并行 → RRF(k≈60) 融合 → cross-encoder 重排。
**Trade-offs**: 四路维护成本和延迟叠加；但免校准融合、互为盲区补充，单路方案在多会话题上明显掉分。

## Pattern 5: Spreading-Activation Graph Retrieval（扩散激活图检索）
**When to use**: 需要召回「文本不相似但共享实体/因果」的间接记忆。
**How**: 语义 top 命中做 BFS 入口；激活 δ ∈ (0,1) 衰减传播；边型乘子 μ(ℓ)——causal/entity >1、弱语义/长程 temporal ≤1。
**Trade-offs**: 图质量决定一切；需要 retain 阶段维护四类边。

## Pattern 6: Hybrid Temporal Parsing（混合时间解析）
**When to use**: 查询含 'last weekend'、'June 2024' 等时间表达。
**How**: 规则日期库先归一化（覆盖多数、低延迟）→ 解析失败回退 seq2seq（flan-t5-small）→ 区间与发生区间重叠匹配 → 中点距离打分；图遍历限制在命中集内。
**Trade-offs**: 多一个模型依赖；换来时间题从 31.6%→79.7% 级别的召回改善。

## Pattern 7: Disposition-Conditioned Generation（画像条件化生成）
**When to use**: agent 需要跨会话稳定的性格与立场。
**How**: 数值画像 Θ=(S,L,E,β) 持久化在 bank profile；ϕ 把它自然语言化进系统消息；β 控制立场强度（0 客观 / 0.5 平衡 / 1 鲜明）。
**Trade-offs**: 极端画像会偏移内容；事实型任务用中性档（S=L=E=3, β=0.2）。

## Pattern 8: Opinion Formation & Reinforcement（观点形成与强化）
**When to use**: agent 要有可演化、可追溯的信念。
**How**: 形成——reflect 时第一人称抽取 + 置信度；强化——retain 时实体+语义筛候选、LLM 判 {reinforce, weaken, contradict, neutral}、c 按 α 步长调整，强矛盾可改文本。
**Trade-offs**: α 小则稳但迟钝，大则灵但震荡；信念演化需要独立存储而不是散在生成文本里。

## Pattern 9: LLM Background Merge（LLM 背景合并）
**When to use**: 用户画像/背景会随时间追加信息。
**How**: 新片段先归一第一人称 → LLM 合并：冲突以新为准、非冲突追加、保持 'I'、控制在几百字符。
**Trade-offs**: 比规则覆盖多一次 LLM 调用；避免拼接导致的提示词膨胀与自相矛盾。

## Pattern 10: Async Observation Regeneration（异步观察重算）
**When to use**: 实体摘要类的派生数据。
**How**: 写入路径只做主记录；新事实触发后台任务重算该实体的 observation（物化视图思路）。
**Trade-offs**: 读到的摘要可能短暂落后；换写入低延迟与摘要渐进变好。

## Pattern 11: Type-Checked LLM Outputs（Pydantic 结构化输出）
**When to use**: LLM 输出要进库或进程序逻辑。
**How**: Literal 类型锁 fact_type/relation_type，范围约束锁 confidence/strength；抽取与观点分离两个 schema。
**Trade-offs**: schema 变更要同步提示词；换来解析零脆弱性。

## Pattern 12: Same-Backbone Ablation（同底模对照评测）
**When to use**: 证明性能来自架构而非模型规模。
**How**: 同一底模跑有记忆/无记忆两组（39.0% vs 83.6%）；裁判统一、temperature=0；基线注明来源（报告引用/榜单自称）。
**Trade-offs**: 引用他家基线时裁判不同源，跨行比较需标注局限。
