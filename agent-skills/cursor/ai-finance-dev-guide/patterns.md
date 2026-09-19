# Patterns — AI 金融项目开发指南

## 契约先行 + Mock 并行
**When to use**: 前后端/Agent 互相阻塞时  
**How**: 定 API+工具 Schema → Swagger/Mock → 各自实现 → 契约测试  
**Trade-offs**: 前期讨论成本 ↑，集成期返工 ↓

## 公共能力单点实现
**When to use**: 多 Agent 共用 LLM/记忆/日志  
**How**: 4.2 Owner 表；改契约先文档后代码  
**Trade-offs**: 集成负责人瓶颈；需严格 Review

## LLM 决策树（确定性优先）
**When to use**: 新需求是否上模型  
**How**: 确定输出→规则；可查→NL2SQL/API；否则 LLM+兜底+评测  
**Trade-offs**: 规则维护成本；合规场景必须前两层

## Prompt 版本化回归
**When to use**: 任何 Prompt/Few-shot 变更  
**How**: app/prompts/ + Owner + PR + 同一黄金集重跑  
**Trade-offs**: 迭代变慢；避免 silent 退化

## 上下文预算与记忆分层
**When to use**: 多轮/多 Agent 上下文膨胀  
**How**: 短 Redis / 中 MySQL / 长向量；重排+预算；跨 Agent 传结论+ID  
**Trade-offs**: 工程复杂；降 Token 与准确率平衡

## 非确定性测试（节点序列）
**When to use**: Agent/LangGraph 编排  
**How**: 断言访问节点序列；注入超时/空结果/报错；temperature=0  
**Trade-offs**: 无法断言全文；需维护评测集

## 小步 Todo + 单步 Commit
**When to use**: 初级团队并行开发  
**How**: 0.5–2h 一步，含输出与自测；一 commit 一步  
**Trade-offs**: commit 多；冲突粒度细易定位

## 演示四时点预案
**When to use**: 答辩/对外演示前  
**How**: T-3 新机 15min 拉起；T-1 视频；T-30 必问句；现场不改代码  
**Trade-offs**: 准备时间；换 -20 风险

## 反馈→归类→评测集
**When to use**: 线上点踩/转人工  
**How**: trace_id 关联；归类根因层；进需求或黄金集非只改 Prompt  
**Trade-offs**: 需流程纪律

## Git Flow 简化版
**When to use**: 7 人教学/中小团队  
**How**: feature→develop→PR→main；禁直推；Tag 发布  
**Trade-offs**: develop 分支可选；策略选定后不混用
