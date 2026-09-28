# Chapter 9: Code Availability & Conclusion

## Core Idea
实现与评测全开放（GitHub 仓库 + 可下钻的结果查看器）；结论重申「记忆是一等推理底座」，并点出四个未来方向：联合优化、RL 循环、工具/工作流集成、可控遗忘与隐私记忆。

## Frameworks Introduced
- **开源交付三件套（§8）**:
  - 代码仓库: https://github.com/vectorize-io/hindsight —— 含完整记忆架构（retain/recall/reflect 流水线 + 四网络表示）、跑 LongMemEval/LoCoMo 的脚本与配置（可换骨干与裁判设置）、事实抽取/图构建/检索分析工具。
  - 交互式结果查看器: https://hindsight-benchmarks.vercel.app/ —— 逐题结果下钻、检索到的记忆上下文、模型与裁判配置、各变体聚合指标。
  - 论文 §8 明说复现路径：下载代码 → 按文中基准重跑。

## Conclusion 的四条主张（§9）
1. HINDSIGHT 把记忆当一等推理底座而非薄检索层——四网络（原文结论处写作 world/bank/observation/opinion，bank 即 experience）分离证据、摘要、信念。
2. 三操作显式化后仍兼容现代 LLM。
3. 实验表明这种结构在实践中「clearly leads to significant improvements」。
4. 结构本身（不是模型规模）是性能来源——同底模对照支撑。

## Future Directions（四个方向）
1. **联合优化**: 不再把事实抽取、图构建、检索当固定流水线，而是端到端学习——嘈杂开放域场景下更能提升鲁棒与效率。
2. **RL 循环**: 用强化学习探索 retain/recall/reflect 三者的交互（论文点名为 ideal 的探索方式）。
3. **工具与工作流**: 与更丰富的 tool-use、workflow orchestration 集成，超越对话类基准。
4. **信念层扩展**: controlled forgetting（可控遗忘）、time-aware belief revision（时间感知信念修订）、privacy-aware memory management（隐私感知记忆管理）——通往长寿命 agent 的路径。

## Key Concepts
- **First-class substrate（一等底座）**: 记忆不是模型外面的插件，而是推理发生在其上的结构化层。
- **Open evaluation（开放评测）**: 结果查看器允许逐题核对，比只给聚合数字更可审计。

## Mental Models
- 把四个未来方向读成当前架构的四个已知边界：流水线固定（→联合优化）、三操作无学习信号（→RL）、只测对话场景（→工具/工作流）、观点只增不删（→可控遗忘/隐私）。

## Anti-patterns
- **只引用聚合分数不查逐题**: 查看器存在的意义就是让引用者能核对检索上下文与裁判配置。
- **把 bank network 和 experience network 当两个东西**: 论文两处命名不一致（§3 叫 experience，结论叫 bank），指同一张网络。

## Key Takeaways
1. 复现入口: github.com/vectorize-io/hindsight + hindsight-benchmarks.vercel.app。
2. 结论自评的边界诚实可查：对话基准之外（工具使用、工作流）尚未验证。
3. 「可控遗忘」被列为未来工作——意味着当前实现的记忆只增不删，隐私场景不能直接上。

## Connects To
- **Ch 8**: 代码与查看器是实验数字的支撑材料
- **Ch 3**: 结论呼应四网络/三操作的初始抽象
- **Ch 10**: 附录提示词是仓库 prompt 文件的论文版
