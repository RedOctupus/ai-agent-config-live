---
name: ai-agents-in-depth-zh-cn
description: "知识库来自《深入理解 AI Agent：设计原理与工程实践》（李博杰 著）。用于在 AI Agent 架构、上下文工程、记忆与知识库、工具设计、Coding Agent、评估、模型后训练、持续进化、多模态实时交互、多 Agent 协作等主题上参考本书框架、原则与工程模式。"
---

<!-- argument-hint: [topic, framework name, chapter number, or concept] -->

# 深入理解 AI Agent：设计原理与工程实践
**Author**: 李博杰 | **Pages**: ~314 | **Chapters**: 10 | **Generated**: 2026-09-04

## How to Use This Skill

- **Without arguments** — load the core frameworks and mental models for reference.
- **With a topic** — ask about `ReAct`, `上下文工程`, `RAG`, `MCP`, `Coding Agent`, `模型后训练`, `多 Agent 协作` or another indexed topic; I will read the relevant chapter before answering.
- **With a chapter** — ask for `ch05` or `第5章` to load that specific chapter summary.
- **Browse** — ask "what chapters do you have?" to see the full index.

When you ask about a topic not covered in Core Frameworks below, I will read the relevant chapter file before answering.

---

## Core Frameworks & Mental Models

- **Agent = LLM + 上下文 + 工具**：Agent 的三元公式。LLM 是大脑（决策），上下文是眼睛（观察），工具是手脚（行动）。三者协同才能从被动问答走向自主执行。
- **Harness 工程**：模型能力只是地基，工程封装（提示词、工具、编排、缓存、评估、护栏）才是产品竞争力的核心。
- **上下文决定能力上限**：中等模型 + 好上下文 > 顶级模型 + 坏上下文。上下文工程不是多塞信息，而是系统性地组织信息供给。
- **工具设计是行动空间的边界**：工具的通用性、粒度、描述精度、安全约束直接决定 Agent 能走多远。MCP 是统一工具生态的关键标准。
- **Coding Agent 是通用 Agent 的元能力**：七个基础工具（Code Interpreter、Bash、Read/Write/Edit、Glob、Grep）组合起来可完成大量任务；代码让思考精确、可执行、可验证。
- **评估要评系统，不是只评模型**：模型替换 + 消融实验帮助区分瓶颈在模型还是 Harness；Rubric 逐项评分、幻觉作为否决项。
- **SFT 记忆，RL 泛化**：预训练 → SFT → RL 三阶段流水线；数据和环境比算法更重要；能用上下文工程解决的不要微调。
- **持续进化 = 评价 + 抽象 + 验证 + 发布**：保存经历不等于学习。需要三层轨迹验证（结果/过程/质量），从知识/指令/程序/参数四个层面选择更新，并经过回归和灰度。
- **实时交互需要快慢思考解耦**：语音/Computer Use/机器人控制需要低延迟快思考，复杂推理交给后台模型，通过 Latent Bridge 传递结果。
- **多 Agent 协作的核心是上下文共享 vs 隔离**：默认隔离上下文，通过共享文件系统或消息总线显式通信；专业化 + 协调 = 群体智能。

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-ai-agent-ru-men.md) | AI Agent 入门 | Agent = LLM + 上下文 + 工具；ReAct；工具五类；Harness 工程 |
| [ch02](chapters/ch02-shang-xia-wen-gong-cheng.md) | 上下文工程 | 消息四角色；KV Cache；Prompt Cache；系统提示词四维设计；Skills；压缩策略 |
| [ch03](chapters/ch03-yong-hu-ji-yi-he-zhi-shi-ku.md) | 用户记忆和知识库 | 用户记忆 vs 知识库；RAG；混合检索；RAPTOR/GraphRAG；双层记忆架构 |
| [ch04](chapters/ch04-gong-ju.md) | 工具 | 工具五类；MCP；通用 vs 专用工具；事件驱动；主动工具发现 |
| [ch05](chapters/ch05-coding-agent.md) | Coding Agent 与代码生成 | 七个核心工具；代码作为元能力；Sessionless；沙箱安全 |
| [ch06](chapters/ch06-ping-gu.md) | Agent 的评估 | 三层评估体系；Rubric；LLM-as-a-Judge；模型替换/消融；统计显著性 |
| [ch07](chapters/ch07-hou-xun-lian.md) | 模型后训练 | 预训练/SFT/RL；SFT 记忆 vs RL 泛化；数据环境 > 算法 |
| [ch08](chapters/ch08-chi-xu-jin-hua.md) | Agent 的持续进化 | 持续进化闭环；三层轨迹验证；四层候选更新；回归/灰度/回滚 |
| [ch09](chapters/ch09-duo-mo-tai-yu-shi-shi-jiao-hu.md) | 多模态与实时交互 | 语音三代架构；全双工；快慢思考解耦；Computer Use；机器人控制 |
| [ch10](chapters/ch10-duo-agent-xie-zuo.md) | 多 Agent 协作 | 共享 vs 隔离上下文；IPC 范式；消息总线；角色化分解 |

---

## Topic Index

- **Agent 架构** → ch01, ch02, ch04, ch05
- **上下文工程** → ch02
- **上下文压缩** → ch02
- **工具调用** → ch01, ch04
- **工具设计** → ch04
- **MCP** → ch04
- **Coding Agent** → ch05
- **代码生成** → ch05
- **沙箱安全** → ch05
- **用户记忆** → ch03
- **知识库** → ch03
- **RAG** → ch03
- **混合检索** → ch03
- **GraphRAG** → ch03
- **评估** → ch06
- **Rubric** → ch06
- **LLM-as-a-Judge** → ch06
- **消融实验** → ch06
- **模型替换** → ch06
- **预训练** → ch07
- **SFT** → ch07
- **RL** → ch07
- **持续进化** → ch08
- **轨迹验证** → ch08
- **回归测试** → ch06, ch08
- **多模态** → ch09
- **实时交互** → ch09
- **语音交互** → ch09
- **Computer Use** → ch09
- **全双工** → ch09
- **多 Agent 协作** → ch10
- **消息总线** → ch10
- **共享上下文** → ch10
- **隔离上下文** → ch02, ch10
- **Harness 工程** → ch01, ch06
- **ReAct** → ch01
- **Prompt Injection** → ch02
- **KV Cache** → ch02
- **Prompt Cache** → ch02

## Supporting Files

- [glossary.md](glossary.md) — 所有关键术语及定义
- [patterns.md](patterns.md) — 32 个设计模式、算法与工程实践
- [cheatsheet.md](cheatsheet.md) — 决策规则、决策树、权衡矩阵、阈值与反模式信号

---

## Scope & Limits

This skill covers the book content only. It is generated from the Chinese edition of *AI Agents in Depth* by 李博杰, using a `pypdf` fallback extraction (Docling was not installed), so tables and code blocks may be less layout-precise than a full technical extraction. For hands-on implementation in your codebase, combine with project-specific tools. For topics beyond this book, check related skills or ask the agent directly.
