# Chapter 6: CARA — Coherent Adaptive Reasoning Agents (Reflect)

## Core Idea
CARA 把 agent 的行为画像当成系统配置的一等公民（而不是提示词装饰）：同一份事实，不同画像产生不同观点；观点带置信度存进 opinion 网络，随新证据强化或削弱，形成轨迹而非静态标签。

## Frameworks Introduced
- **动机对照（§5.1）**: 同一 agent 聊远程办公——画像 (S=1, L=2, E=5) 形成「Remote work enables creative flexibility and spontaneous innovation」；画像 (S=5, L=5, E=1) 形成「Remote work lacks the structure and accountability needed for consistent performance」。事实相同，画像决定权重分配（灵活性 vs 结构性）和结论方向。
- **行为画像 Θ = (S, L, E, β)**（§5.2.1）:
  - **Skepticism S ∈ [1,5]**: 高=审慎评估、强调证据质量、拒绝无支撑陈述；低=信任、探索式。
  - **Literalism L ∈ [1,5]**: 高=紧扣字面与显式指令；低=读弦外之音、推断隐含目标。
  - **Empathy E ∈ [1,5]**: 高=考虑情绪语境、支持性与保全面子的语言；低=直白、任务优先。
  - **Bias strength β ∈ [0,1]**: 画像影响观点形成的强度——β=0 以事实为主，β=0.5 中等影响，β=1 强偏好条件化。
  - 选这三维的理由: 紧凑、可解释、可自然语言化（如「skeptical but highly empathetic」）、用户配置直觉。
- **Bank profile（§5.3）**: tuple (n, Θ, h)——名字 n、画像 Θ、第一人称短背景 h。
- **Verbalization ϕ: Θ → String**（§5.3.1）: 把数值画像转成描述文本注入系统消息——数值配置靠这一步才作用到 LLM 行为。
- **Opinion 结构（§5.4.1）**: o = (t, c, τ, b, E)——观点文本（含简短理由）、置信度 c ∈ [0,1]、形成时间戳、库 ID、涉及实体集。
- **Opinion formation 四步（§5.4.2）**: ① Recall(B,Q,k) 取回事实与既有观点 FQ ② 构造系统消息 s = (n, h, ϕ(Θ)) ③ LLM 反思一步同时产出自然语言回答 r 和候选观点更新（条件于 s、FQ、Θ） ④ 解析结构化输出，新/更新观点存入 O。β 决定 s 的措辞：低 β 强调客观、高 β 明确鼓励带立场的表达。
- **Opinion reinforcement 三步（§5.5）**: 新事实经 retain 到来时——
  1. **识别候选**: 实体重叠 + 语义相似（余弦 sim(vo, vf) > 阈值 θ）筛出可能相关的观点；
  2. **评估证据**: LLM 判定 Assess(o, f) ∈ {reinforce, weaken, contradict, neutral}；
  3. **应用更新**: c′ = c + α·Δ，α ∈ (0,1) 是步长；强矛盾/精炼时也可改观点文本 t。
  - 设计意图: 小证据小改动（防止单个反例引起观点震荡），反复强化或强矛盾才能大幅移动；更谨慎的画像可用更小的 α。
- **Background merging（§5.6）**: 新背景片段与旧背景矛盾时用 LLM 合并 h′ = Merge_LLM(h, h_new)——四条规则: ① 直接冲突在适当时以新信息为准 ② 非冲突细节追加 ③ 保持第一人称（'I' 不是 'You'） ④ 简洁（几百字符内）。预处理先把你提供的片段归一化成第一人称。

## Key Concepts
- **Disposition-profile integration（画像集成）**: 行为配置是系统参数，不是每次手写提示词。
- **Opinions as trajectories（观点即轨迹）**: c 随时间演化，能追踪「agent 多坚定」而不只「agent 说什么」。
- **Four CARA capabilities**: 画像集成、HINDSIGHT 记忆集成、观点形成与强化、背景合并与冲突消解。

## Mental Models
- 把 β 想成「立场旋钮」：0 是播音员（只报事实），1 是评论员（鲜明观点），0.2 是论文实验用的中性档。
- 把 opinion 网络想成带置信度的贝叶斯信念表：evidence 不直接改结论，而是走 α 步长改 confidence。
- 把背景 h 想成单行的用户 profile 字段：合并策略 = 冲突覆盖 + 追加，而不是无限拼接（拼接会让提示词膨胀且自相矛盾）。

## Worked Example 1 — 同事实双画像（Figure 5）
- 信任/灵活/共情 (S=1, L=2, E=5) → 观点:「Remote work is a net positive because it removes commute time and creates space for more flexible, self-directed work.」强调自主、灵活、创造自由。
- 怀疑/字面/超然 (S=5, L=5, E=1) → 观点:「Remote work risks undermining consistent performance because it makes it harder to maintain structure, oversight, and shared routines.」强调结构、问责、一致性。

## Worked Example 2 — 背景合并（Figure 6）
- 当前背景: 「I was born in Colorado.」
- 新片段: 「You were born in Texas and have 10 years of startup experience.」（预处理成第一人称）
- 合并后: 「I was born in Texas and have 10 years of startup experience.」——出生地冲突以新信息为准，新增工作经历被保留。

## Worked Example 3 — 观点演化（§5.7.1）
初始观点「Python is better for data science…」(c≈0.8) → 新事实: Python 在 AI/ML 生态占主导 → c 小幅上升 → 后续事实: Julia/Rust 在特定领域有性能优势、替代品采用增长 → c 下降且文本改为更限定的说法。观点从静态标签变成有方向的轨迹。

## Anti-patterns
- **画像当提示词装饰**: 每次会话临时写「你是一个…」，跨会话不一致——偏好一致性靠 bank profile 持久化保证。
- **新背景直接拼接**: 'born in Colorado' 和 'born in Texas' 并存，提示词自相矛盾。
- **观点生成后不更新**: c 永远停在初值，等于没有信念系统，只有立场快照。
- **把「无法回答」当观点抽取**: 附录 A.2 明确排除 'I don't have enough information' 这类语句。

## Key Takeaways
1. 行为画像 = 4 个数值参数，经 ϕ 自然语言化进系统消息——可配置、可复现、可版本化。
2. 形成 (formation) 和强化 (reinforcement) 是两条独立入口：前者在 reflect 时、后者在 retain 时，共同维持观点演化。
3. 更新规则的小步长 α 保证观点「稳定但响应」——这是 preference consistency 和 belief revision 的平衡点。
4. 背景合并的第一人称归一化是便宜但关键的预处理，否则合并函数会在人称上反复纠错。

## Connects To
- **Ch 3**: 本章是 Reflect(B,Q,Θ)→(r,O′) 的实现
- **Ch 4**: reinforcement 由 retain 的新事实触发
- **Ch 7**: reflect 在端到端系统里的五步流水线
- **Ch 10**: 观点形成提示词与 Opinion schema 原文
