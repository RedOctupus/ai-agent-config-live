# Chapter 5: 模块与任务拆分

## Core Idea
按模块小步交付，P0 定基线后 P1–P5 每周一 Phase；前期按**模块**分工建公共能力，后期按 **Agent** 认领演示场景，任务 ≤1 天且带可验证输出。

## Frameworks Introduced
- **P0–P5 排期**: P0 需求+契约+评测基线；P1 工程+RAG+客服；P2 画像+分析；P3 投顾+操作；P4 风控+记忆+安全；P5 集成评测答辩。
- **分工两阶段**: 模块分工（P1–P2）→ Agent 分工（P3–P5）；避免重复 LLM/记忆/工具层。
- **人数合并规则**: 3–7 人按角色池合并，**公共能力 Owner 不可空缺**，五 Agent 归属清晰。
- **个人 Todo 四要素**: 做什么、输出物、自测方式、建议 commit message；0.5–2 小时一步。

## Worked Example
RAG 客服 Todo 链: ChatRequest 模型 → knowledge_search pytest → 串联 RAG+LLM → 低置信兜底 — 每步单独 commit。

## Anti-patterns
- **第一周写完所有 Agent**
- **「大家一起写客服」** 无唯一负责人

## Key Takeaways
1. 拆任务三问: 谁负责、完成后看见什么、怎么证明没坏
2. 小步提交: 能启动、自测过、不提交 .env/大文件
3. 看板: 待办/进行中/待 Review/已完成

## Connects To
- **Ch 6**: feature 分支与 PR
- **Ch 9**: DoD 与自测命令
