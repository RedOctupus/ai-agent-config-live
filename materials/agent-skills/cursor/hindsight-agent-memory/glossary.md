# Glossary

**Abstention (ABS)** — LongMemEval 五能力之一：信息缺失时正确拒答而非猜测 (Ch 8)。
**Background merging** — LLM 把新背景片段并入旧背景：冲突以新为准、非冲突追加、保持第一人称、控制在几百字符内 (Ch 6)。
**Bank profile** — 记忆库画像 tuple (n, Θ, h)：名字、行为画像、第一人称背景 (Ch 6)。
**Bias strength (β)** — 0–1 参数，控制行为画像影响观点形成的强度；0=事实为主，1=强偏好条件化 (Ch 6)。
**Causal link** — LLM 抽取的因果边，权重 1.0，类型 ∈ {causes, caused_by, enables, prevents}，遍历时加权 (Ch 4)。
**Coarse-grained chunking** — 每次对话抽 2–5 条叙事事实而非逐句切分的分块策略 (Ch 4)。
**Confidence score (c)** — 观点置信度 ∈ [0,1]，表征信念强度，随证据强化/削弱 (Ch 3, Ch 6)。
**Coreference resolution** — 共指消解：把 'my roommate' 与 'Emily' 链成同一实体；附录标为 CRITICAL (Ch 4, Ch 10)。
**Cross-encoder reranking** — 用 cross-encoder/ms-marco-MiniLM-L-6-v2 对 RRF 后的候选联合编码重排，拼入时间信息 (Ch 5)。
**Disposition parameters (S, L, E)** — 1–5 三维画像：skepticism 怀疑、literalism 字面、empathy 共情 (Ch 6)。
**Entity resolution (ρ)** — mention → canonical entity 的映射，按字符串相似、共现、时间邻近加权最大化 (Ch 4)。
**Epistemic clarity** — 设计原则：结构上分离证据、摘要、信念，让「知道 vs 相信」可见 (Ch 3)。
**Experience network (B)** — 第一人称自身经历网络 (Ch 3)。
**Fact type (ℓ)** — 事实分类 {world, experience, opinion, observation}，决定入哪张网络 (Ch 3, Ch 4)。
**Full-context baseline** — 整段历史原样入提示词、无结构记忆的对照组 (Ch 1)。
**HNSW + pgvector** — 语义通道的向量索引实现 (Ch 5)。
**LLM-as-a-judge** — 用独立裁判模型对回答二元打分（temperature=0）的评测法 (Ch 8)。
**LongMemEval** — 长程对话基准：500 题、五能力、S≈115k/M≈1.5M token (Ch 8)。
**LoCoMo** — 50 段人-人长对话基准，平均 304.9 轮、19.3 sessions、含图片 (Ch 8)。
**Memory bank (B)** — 命名容器：四网络 + agent profile (Ch 3)。
**Memory unit** — 记忆元组 (u, b, t, v, τs, τe, τm, ℓ, c, x)，一条事实只入一张网络 (Ch 4)。
**Narrative fact** — 自包含、含全部参与者与推理链的完整叙事事实，与碎片化抽取相对 (Ch 4)。
**Observation network (S)** — 偏好中立的实体摘要网络，事实变了异步重算 (Ch 3, Ch 4)。
**Occurrence interval (τs, τe) vs mention time (τm)** — 事情发生区间 vs 被提及时间；区间重叠支持历史查询 (Ch 3)。
**Opinion network (O)** — 带置信度与时间戳的主观信念网络 (Ch 3)。
**Opinion reinforcement** — 新事实到来时三步更新观点：候选识别 → 证据评估 {reinforce, weaken, contradict, neutral} → α 步长更新 c (Ch 6)。
**Preference consistency** — 跨交互保持稳定推理风格与立场的能力 (Ch 1, Ch 3)。
**Reciprocal Rank Fusion (RRF)** — 按名次融合：Σ 1/(k + rank)，k≈60；免校准、容忍缺失 (Ch 5)。
**Reflect(B, Q, Θ)** — 按画像生成响应并更新观点网络的操作 (Ch 3, Ch 7)。
**Retain(B, D)** — 抽取、分类、建图、强化观点、合并背景的写入操作 (Ch 3, Ch 7)。
**Recall(B, Q, k)** — 四路检索 + 融合 + 重排，返回 token 总量 ≤ k 的事实集合 (Ch 3, Ch 5)。
**Spreading activation** — 图通道算法：语义命中做入口 BFS，激活沿边衰减传播，causal/entity 边乘子 >1 (Ch 5)。
**TEMPR** — Temporal Entity Memory Priming Retrieval，实现 retain/recall 的组件 (Ch 4–5)。
**CARA** — Coherent Adaptive Reasoning Agents，实现 reflect 的组件 (Ch 6)。
**HINDSIGHT** — 论文提出的记忆架构：四网络 + 三操作 (全书)。
**Temporal parser (hybrid)** — 规则日期解析优先、flan-t5-small 兜底，把时间表达归一成区间 (Ch 5)。
**Token budget (k)** — 调用方指定的检索 token 上限，替代固定 top-k (Ch 5)。
**Verbalization (ϕ)** — 把数值画像 Θ 转成自然语言描述注入系统消息的函数 (Ch 6)。
**World network (W)** — 客观世界事实网络 (Ch 3)。
