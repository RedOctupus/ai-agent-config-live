# Chapter 10: Appendix A — System Prompts, Judge Prompts, Output Schemas

## Core Idea
附录给出四类提示词（事实抽取、观点形成、观察生成、评测裁判）和三个 Pydantic schema——这是把前文抽象落地时「提示词长什么样」的官方答案，可直接移植到自己的实现。

## Frameworks Introduced
- **A.1 事实抽取提示词（TEMPR）**: 把对话转成结构化叙事事实，硬性要求五个维度全部保留、最大冗余：
  1. **what**：完整描述，含全部对象、动作、数量、细节——NEVER SUMMARIZE OR OMIT；
  2. **when**：必须带星期几，格式 `day_name, month day, year`（如 'Saturday, June 9, 2024'）；
  3. **where**：具体地点/区域（如适用）；
  4. **who**：全部人/实体及完整关系与背景；
  5. **why**：全部情绪、偏好、动机、重要性、细微差别——助手侧事实必须包含触发它的用户请求。
  另加 fact_type、fact_kind、entities、occurred_start/end（结构化日期）、where（结构化地点）。
  **共指消解标为 CRITICAL**：'my roommate Emily' 里通用关系和名字必须链接——正例「Emily (the user's roommate) got married」，反例是当成两个人。
- **A.2 观点形成提示词（CARA）**: 从生成的回答中提取观点并**改写成第一人称**（"I think… / I believe… / In my view… / Previously I thought… but now…"）。
  - 排除项：'I don't have enough information'、'I cannot answer because…' 这类**不是**观点，不抽取。
  - 禁止第三人称（'The speaker thinks…'）；理由要自然嵌在句子里；必须给 0.0–1.0 置信度。
  - 正例风格：「I think Alice is more reliable because she consistently delivers on time and writes clean code」；观点允许演化措辞：「Previously I thought all engineers were equal, but now I feel that experience and track record really matter」。
- **A.3 观察生成提示词（TEMPR）**: 「客观观察者」角色，从实体事实列表合成 3–7 条观察。
  - 七条准则：只写事实、可合并相关事实、不加观点/判断/解读、只写已知不写假设、覆盖身份/特征/角色/关系/活动、第三人称（'John is…'）、冲突事实取最新或最有支撑的。
  - 反例三连：'John seems like a good person'（评价）、'John probably likes his job'（假设）、'I believe John is reliable'（第一人称观点）。
- **A.4 LongMemEval 裁判提示词（5 类）**: 统一模式——给 question、correct answer、model response，答 yes/no，**必须以 `\boxed{yes}` 或 `\boxed{no}` 结尾**；等价答案或含全部中间步骤都算对，只给部分信息算错。
  - **单/多会话题**: 标准版。
  - **时间推理题**: 额外豁免——天/周/月数量差 ±1（off-by-one）不扣分。
  - **知识更新题**: 同时含旧信息和更新后答案算对，只要更新答案是要的那个。
  - **偏好题**: 输入是 rubric 而非标准答案——不要求覆盖全部要点，正确召回并使用了用户个人信息即算对。
  - **弃答题**: 给不可回答的问题 + 解释，模型正确识别「信息不全/答非所问」即对。
- **A.5 结构化输出 schema（Pydantic）**:
  - `ExtractedFact`: what/when/where/who/why 五个必填 str + `fact_type: Literal["world","experience","opinion"]`（注意：schema 里没有 observation，由观察生成单独走 A.3）+ 可选 occurred_start/occurred_end/mentioned_at/entities/causal_relations；`CausalRelation` = (target_fact_index, relation_type ∈ {causes, caused_by, enables, prevents}, strength ∈ [0,1])。
  - `Opinion` = (opinion, confidence ∈ [0,1], reasoning)；`OpinionExtractionResponse` = opinions 列表。
  - `Observation` = (observation)；`ObservationExtractionResponse` = observations 列表。

## Key Concepts
- **Verbosity requirement（冗余要求）**: 「More detail is ALWAYS better than less」——抽取阶段宁多勿少，检索阶段再用预算裁剪。
- **First-person normalization（第一人称归一化）**: 观点必须以「我」表述，保证存进 O 网络的条目与 bank 身份一致。
- **Boxed final answer（盒装最终答案）**: 裁判输出格式约束，方便程序化解析。

## Mental Models
- 把四组提示词想成四道「质检关卡」：抽取关卡验五维齐全，观点关卡验人称与置信度，观察关卡验无评价词，裁判关卡验格式可解析。
- schema 是提示词的可执行版本：Literal 类型把「分到哪张网络」从自然语言要求变成硬校验。

## Worked Example — ExtractedFact 的一次填值
输入「My roommate Emily got married last Saturday at Google HQ, she seems happy」→ what: Emily 结婚全程细节；when: 'Saturday, June 8, 2024'（带星期）；where: Google HQ；who: Emily（user's roommate）；why: 情绪/意义；fact_type: "world"；entities: [Emily(PERSON), Google(ORGANIZATION)]。'seems happy' 若是模型推断而非陈述，按 A.3 规则不进观察、也不当观点。

## Anti-patterns
- **抽取阶段摘要压缩**: 与整套架构对着干——长程问题需要的细节常在被压掉的从句里。
- **观点用第三人称存库**: 后续强化和合并都以第一人称为前提，第三人称会破坏背景一致性。
- **裁判提示词不锁输出格式**: 没有 `\boxed{}` 就得写脆弱的解析器。
- **把 schema 的 fact_type 当四分类**: Pydantic 里只有 world/experience/opinion——observation 有自己的生成路径。

## Key Takeaways
1. 五维抽取（what/when/where/who/why）+ 星期几时间格式是事实质量的最低标准。
2. 观点与观察的分界线在提示词层就划死：第一人称+置信度=观点；第三人称+无评价=观察。
3. 裁判的五种题型变体说明：评测的公平性写在提示词细节里（off-by-one 豁免、rubric 容错、更新答案算对）。
4. 想复现或移植 HINDSIGHT，附录四组提示词 + 三个 schema 是最短路径。

## Connects To
- **Ch 4**: A.1、A.3、A.5 是 retain 抽取步骤的实现原文
- **Ch 6**: A.2 是 opinion formation 第 3 步的提示词
- **Ch 8**: A.4 是 LLM-as-a-judge 的实现原文
