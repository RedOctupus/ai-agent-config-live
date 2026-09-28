# Chapter 7: Unified HINDSIGHT Architecture — Putting It All Together

## Core Idea
端到端只有一条环：原始对话 → retain 结构成图 → 需要时 recall 预算内取回 → reflect 带画像作答并更新信念；本章把三操作展开成可照着实现的编号流水线。

## Frameworks Introduced
- **Retain 流水线（5 步）**: 给定记忆库 B 和输入数据 D，输出更新后的四网络 M′：
  1. LLM 事实抽取（带时间区间）把 D 转成结构化事实集 F = {f1,…,fn}；
  2. 实体识别与消解，把 mention 映射到 canonical 实体 E；
  3. 图链接构建——temporal、semantic、entity、causal 四类边写入 G=(V,E)；
  4. 自动观点强化：对每个既有观点 o ∈ O 找相关新事实、按 Ch 6 的规则更新置信度；
  5. 背景合并 h′ = Merge_LLM(h, h_new) 保持 bank profile 一致。
- **Recall 流水线（4 步）**: 给定 B、Q、token 预算 k，返回 Σ|fi| ≤ k 的有序事实：
  1. 四路并行检索（semantic / keyword / graph / temporal）产出候选 Rsem, Rbm25, Rgraph, Rtemp；
  2. RRF 融合四张排名表；
  3. cross-encoder 神经重排给最终精度（CE(Q,f) 打分）；
  4. token 预算过滤——按名次贪心选取直到预算耗尽。
- **Reflect 流水线（5 步）**: 给定 B、Q、画像 Θ，输出响应 r 和更新后的观点网络 O′：
  1. 调 TEMPR 取回四网络记忆 FQ = Recall(B,Q,k)；
  2. 加载 bank 画像 Θ=(S,L,E,β) 和背景 h；
  3. 按 s = Verbalize(n, h, Θ) 条件化生成响应（语气与论证受 β 调制）；
  4. 适当时形成新观点 (t, c, τ, b, E) 并加入 O；
  5. 存储供未来检索与强化，O′ = O ∪ {o1,…,om}。

## Key Concepts
- **Full loop（完整闭环）**: 新经历被 retain 成结构化记忆 → 按需 recall → reflect 更新信念与身份配置——每一次作答都改变下一次作答的输入。
- **System-level properties（系统级性质）**: 论文主张这些性质来自组件交互而非单组件——证据/摘要/信念分离、时间与实体感知的召回、偏好一致的可追溯作答。

## Mental Models
- 把整套系统想成「带记忆的操作系统」：retain 是 write path（含触发器：观点强化、后台观察重算），recall 是 read path（查询规划器），reflect 是进程（带环境变量 Θ）。
- 闭环的工程含义：写路径和读路径都可能改库（reflect 也写 O′），所以记忆库需要事务性地处理并发的 retain/reflect 写入。

## Worked Example — 一次完整调用
新对话进来 → Retain：抽 3 条叙事事实 → 消解出实体 Alice、E2E 项目 → 建 temporal/entity/causal 边 → 发现与既有观点「Alice 很可靠」相关 → Assess=强化 → c 从 0.7 → 0.78。用户随后问「Alice 负责什么？」→ Recall（预算 k）：BM25 命中专名 + 图通道沿 entity 边捞到跨会话事实 → RRF+重排+装箱 → Reflect：按 Θ 措辞作答，若形成新观点则存入 O′。

## Anti-patterns
- **三操作各自为政**: 抽取的信息和检索需要的信息不匹配（如抽取时不存时间区间，检索时做不了时间通道）——六步流水线的每步都是为下游某通道准备数据。
- **只在 reflect 更新信念**: 论文把 reinforcement 放在 retain 步骤 4——新证据一进来就更新，而不是等被问到才更新。
- **忘掉 reflect 也写库**: O′ 不落盘，下次调用观点演化从头开始。

## Key Takeaways
1. 三操作的实现清单（5+4+5 步）可以直接当开发任务拆解表用。
2. retain 是唯一的数据写入口，但它自带两个副作用：观点强化和背景合并——写路径不纯但有意为之。
3. recall 的预算 k 贯穿全链：reflect 第 1 步就透传调用方的 token 预算。
4. 神经组件（嵌入、重排、LLM）全部可插拔——换骨干不改架构。

## Connects To
- **Ch 3**: 本章是三操作形式定义的工程展开
- **Ch 4–6**: 每一步对应的组件细节
- **Ch 8**: 该流水线在 LongMemEval/LoCoMo 上的实测效果
