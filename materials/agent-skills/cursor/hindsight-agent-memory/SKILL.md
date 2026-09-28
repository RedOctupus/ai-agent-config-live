---
name: hindsight-agent-memory
description: "Knowledge base from \"HINDSIGHT IS 20/20: Building Agent Memory That Retains, Recalls, and Reflects\" by Latimer, Boschi, Neeser et al. (Vectorize.io / Washington Post / Virginia Tech). Use when applying the HINDSIGHT four-network memory architecture, TEMPR/CARA design, retain-recall-reflect operations for agent memory systems, or referencing LongMemEval/LoCoMo results."
---

<!-- argument-hint: [topic, framework name, or chapter number] -->

# HINDSIGHT IS 20/20: Building Agent Memory That Retains, Recalls, and Reflects
**Author**: Chris Latimer, Nicoló Boschi, Andrew Neeser, Chris Bartholomew, Gaurav Srivastava, Xuan Wang, Naren Ramakrishnan | **Pages**: ~28 | **Chapters**: 10 | **Generated**: 2026-09-28

## How to Use This Skill

- **Without arguments** — load core frameworks for reference
- **With a topic** — ask about `opinion-reinforcement`, `rrf`, or another indexed topic; I find and read the relevant chapter
- **With chapter** — ask for `ch05`; I load that specific chapter
- **Browse** — ask "what chapters do you have?" to see the full index

When you ask about a topic not covered in Core Frameworks below, I will read the relevant chapter file before answering.

---

## Core Frameworks & Mental Models

**四网络记忆组织（four-network memory organization）** — 记忆库 M = {W, B, O, S}：
- World W：客观世界事实（与 agent 视角无关）
- Experience B：第一人称自身经历（做过/说过/推荐过）
- Opinion O：主观判断，每条 = (t, c, τ)——观点文本、置信度 c ∈ [0,1]、形成时间戳 τ
- Observation S：从 W/B 合成的偏好中立实体摘要（物化视图，事实变了异步重算）
- 规则：每条事实按 fact_type 只入一张网络。Use this when 设计需要「区分知道 vs 相信」的记忆系统。

**三核心操作（three core operations）** — 形式化读写契约：
- `Retain(B, D) → M′`：抽取叙事事实 → 分类入网 → 建四类图链接 → 触发观点强化 → 背景合并
- `Recall(B, Q, k) → {f1..fn}`：四路并行检索（semantic/keyword/graph/temporal）→ RRF → cross-encoder 重排 → Σ|fi| ≤ k
- `Reflect(B, Q, Θ) → (r, O′)`：recall → 加载画像 → 条件化生成 → 形成/存储新观点
- Think of these as API 契约：每层可单独测试替换；神经组件（嵌入、重排、LLM）全可插拔。

**TEMPR + CARA 双组件**：
- TEMPR（Temporal Entity Memory Priming Retrieval）= retain + recall：LLM 叙事事实抽取、实体消解 ρ、temporal/semantic/entity/causal 四类边、token 预算检索
- CARA（Coherent Adaptive Reasoning Agents）= reflect：行为画像 Θ=(S,L,E,β) 调制生成、观点形成与强化、背景合并

**行为画像 Θ（disposition profile）** — Skepticism/Literalism/Empathy 各 1–5 + bias strength β ∈ [0,1]：
- 数值经 ϕ 自然语言化注入系统消息；β=0 事实为主，0.5 平衡，1 强立场
- 同一事实不同画像 → 不同观点（Fig 5 远程办公对照）；事实型任务锁 S=L=E=3、β=0.2

**观点演化机制（opinion formation & reinforcement）**：
- 形成（reflect 时）：第一人称抽取 + 置信度；'I don't have enough information' 不是观点
- 强化（retain 时）：实体+语义筛候选 → LLM 判 {reinforce, weaken, contradict, neutral} → c += α·Δ（小步长防震荡）
- 设计意图：观点是轨迹不是标签——稳定但响应

**叙事事实抽取（narrative fact extraction）** — 对话按 2–5 条/次粗粒度抽取，每条五维齐全（what/when/where/who/why，时间必须带星期）；共指消解 CRITICAL（'my roommate'=Emily）。反模式：句子级碎片化——丢跨轮推理链。

**四路检索 + RRF**：
| 通道 | 技术 | 补什么 |
|---|---|---|
| Semantic | HNSW/pgvector 余弦 | 改写、同义 |
| Keyword | GIN/BM25 | 专名术语精确匹配 |
| Graph | 扩散激活 BFS（causal/entity 边 μ>1） | 共享实体/因果的间接关联 |
| Temporal | 规则日期解析 + flan-t5-small 兜底 | 时间区间匹配 |
- RRF：名次融合 Σ 1/(k+rank)，k≈60——免校准、容忍缺失；之后必须 cross-encoder (ms-marco-MiniLM-L-6-v2) 重排

**Token 预算接口（agent-optimized retrieval）** — Recall 返回 Σ|fi| ≤ k 而非 top-k：重排决定优先级，贪心装箱执行预算。这是面向 LLM 的检索与面向人眼的检索的根本差别。

**设计四原则**：epistemic clarity（证据/摘要/信念分离）、temporal awareness（τs/τe/τm 三时间戳 + 区间重叠查询）、entity-aware（四类边多跳发现）、preference consistency（画像稳定 + 置信度演化）。

**关键实证（同底模对照）**：LongMemEval S：39.0% → 83.6%（OSS-20B，+44.6 点）→ 89.0%（OSS-120B）→ 91.4%（Gemini-3）；LoCoMo：75.78%（先前最强开源 Memobase）→ 83.18/85.67/89.61%。最大涨幅在长程题：multi-session 21.1→79.7。评测注意：基线引用他家裁判（Supermemory 报告 / Backboard 榜单），HINDSIGHT 自评用统一 GPT-OSS-120B 裁判。

**评测设置**：LLM-as-a-judge 二元打分、temperature=0、`\boxed{yes/no}` 结尾；时间题 ±1 天豁免；偏好题按 rubric 容错；弃答题看是否正确拒答。

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-introduction.md) | Abstract & Introduction | 四网络、三操作、贡献数字 |
| [ch02](chapters/ch02-related-work.md) | Related Work | 竞品二分法、Table 1 对比 |
| [ch03](chapters/ch03-architecture-overview.md) | Overview | 形式定义、设计四原则 |
| [ch04](chapters/ch04-TEMPR-retain.md) | TEMPR Retain | 叙事抽取、实体消解、四类边、observation 范式 |
| [ch05](chapters/ch05-TEMPR-recall.md) | TEMPR Recall | token 预算、四路检索、RRF、重排 |
| [ch06](chapters/ch06-CARA-reflect.md) | CARA Reflect | 画像 Θ、观点形成/强化、背景合并 |
| [ch07](chapters/ch07-unified-architecture.md) | Unified Architecture | 5+4+5 步流水线 |
| [ch08](chapters/ch08-experiments.md) | Experiments | LongMemEval/LoCoMo、Table 2/3/4 |
| [ch09](chapters/ch09-conclusion-code.md) | Code & Conclusion | 仓库、查看器、未来方向 |
| [ch10](chapters/ch10-appendix-prompts.md) | Appendix Prompts & Schemas | 四组提示词、Pydantic schema |

## Topic Index

- **行为画像 / disposition profile** → ch06, ch03
- **background merging** → ch06, ch10
- **CARA** → ch06, ch07
- **四路检索 / four-way retrieval** → ch05, ch07
- **实体消解 / entity resolution** → ch04
- **四网络 / four networks** → ch03, ch01
- **图链接 / link types** → ch04
- **LLM-as-a-judge** → ch08, ch10
- **LongMemEval** → ch08, ch10
- **LoCoMo** → ch08
- **叙事事实 / narrative facts** → ch04, ch10
- **observation 范式** → ch04, ch10
- **opinion 形成与强化** → ch06, ch10
- **RRF** → ch05, ch07
- **TEMPR** → ch04, ch05
- **token 预算** → ch05
- **时间解析 / temporal** → ch05, ch03
- **竞品对比 / related systems** → ch02

## Supporting Files

- [glossary.md](glossary.md) — all key terms with definitions
- [patterns.md](patterns.md) — all techniques and design patterns
- [cheatsheet.md](cheatsheet.md) — quick reference tables and decision guides

---

## Scope & Limits

This skill covers the paper content only (synthesized summaries, not the paper text). For hands-on implementation, the authors' code is at https://github.com/vectorize-io/hindsight with per-question results at https://hindsight-benchmarks.vercel.app/. Note: the paper's retrieval token budgets appear as an unfilled `<add>` placeholder in §7.3 — exact values are unknowable from the text.
