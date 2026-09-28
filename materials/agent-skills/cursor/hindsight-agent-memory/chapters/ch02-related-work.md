# Chapter 2: Related Work — Memory Architectures, Benchmarks, Cognitive Foundations

## Core Idea
现有 agent 记忆研究分两堆：一堆做「怎么存和取」（从分层上下文到时间知识图谱），一堆做「怎么评和类比人脑」；HINDSIGHT 的差异点是同时做到「事实/信念分离 + 行为画像条件化推理 + 观点可演化」。

## Frameworks Introduced
- **Related Work 二分法**: 把竞争工作分成 (1) 记忆架构与系统、(2) 基准与认知基础两类来对比。
  - When to use: 写论文 related work 或给新记忆系统做竞品定位时。
  - How: 每个系统沿固定维度打分（是否分离事实与信念、是否带行为画像、观点是否可演化），填进对比表。
- **对比表维度（Table 1 的隐含 schema）**: ✓/✗ 特征对照——分离客观事实与主观观点、带行为画像的条件化推理、带置信度的观点演化。

## Key Concepts
- **Tiered context management（分层上下文管理）**: MemGPT 把记忆当无结构文本块在主提示词和归档存储间分页，不分离事实与信念；LIGHT 用 episodic/working/scratchpad 缓冲处理千万 token 对话，同样不区分主观信念与客观观察。
- **Temporal knowledge graph（时间知识图谱）**: Zep 用双时态建模（bitemporal）跟踪事实「何时成立」vs「何时被记录」，但只建模客观事实，不建模主观信念与行为画像。
- **Zettelkasten atomic notes（原子笔记）**: A-Mem 用卡片盒法生成原子笔记 + LLM 生成的链接，但所有记忆一视同仁，不分离事实与观点。
- **Fact conflict via DB update（数据库式冲突处理）**: Mem0 遇到事实冲突直接改库，而不是让信念带置信度演化。
- **RL-trained memory operations（强化学习训练记忆操作）**: Memory-R1 用 RL 训练 agent 的记忆读写策略优化 QA 准确率，不关注认知结构与画像一致性。
- **Parametric vs external memory（参数化 vs 外部记忆）**: MemVerse 通过微调把检索记忆并入参数，带来可编辑性问题；HINDSIGHT 只用外部记忆回避这一点。

## Reference Tables

### Table 1 竞品清单（按类别）
| 类别 | 系统 | 机制 | HINDSIGHT 指出的缺口 |
|---|---|---|---|
| 分层上下文 | MemGPT | OS 式内存分页 | 文本块无结构，事实/信念不分 |
| 分层上下文 | LIGHT | 千万 token 三缓冲 | 主客观记忆不分 |
| 知识图谱 | Zep | 双时态时间图 | 不建模信念与行为画像 |
| 知识图谱 | A-Mem | Zettelkasten 原子笔记 | 记忆同质，无事实/观点之分 |
| 生产系统 | Mem0 | 稠密检索+图，改库解决冲突 | 冲突不演化为信念更新 |
| 强化学习 | Memory-R1 | RL 训记忆操作 | 无认知结构、无画像一致性 |
| 参数化 | MemVerse | 双路检索+微调 | 参数化记忆难编辑 |
| 具身 AI | KARMA | 3D 场景图 | 面向机器人，非对话 agent |

### Benchmark 对照
| Benchmark | 规模 | 测什么 |
|---|---|---|
| LoCoMo | 50 对话、最长 35 session | 长程时间/因果推理 |
| LongMemEval | 最高 1.5M token | 信息抽取、跨会话、时间推理 |
| MemoryBench | 反馈式 | 持续学习、反馈利用 |

## Mental Models
- 用「分离轴」判断一个记忆系统是否完备：存储层分不分事实/摘要/信念 → 推理层带不带画像 → 随时间更不更新信念。三个都缺 = 只是检索插件。
- 把 benchmark 当压力测试类型图：LongMemEval 压长上下文稀释，LoCoMo 压真实多会话，MemoryBench 压反馈遗忘。

## Anti-patterns
- **只比准确率不比架构维度**: 论文把 Table 1 的结构特征对比放在准确率表之前——先证明架构有独特能力，再谈分数。
- **拿参数化记忆换可编辑性**: 微调进参数的记忆无法像 opinion 网络那样被逐条更新和追溯。

## Key Takeaways
1. 先前系统的共同缺口是三件事：证据与推断混存、长程组织能力弱、无法解释「为什么这样答」。
2. Zep 的双时态图只解决「事实何时成立」，不解决「agent 何时改变了看法」。
3. 认知科学类比（情景/语义记忆、记忆四面体、显式/隐式记忆）提供了分类法，但都没有给出可实现的信念演化机制。

## Connects To
- **Ch 1**: 三挑战（长程访问、认知区分、偏好一致性）在此展开
- **Ch 3**: HINDSIGHT 如何逐条回应这些缺口
- **Ch 8**: Table 3/4 与这些系统的真实分数对比
