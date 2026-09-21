# Chapter 4: 方案设计与接口契约

## Core Idea
并行开发的前提是**公共能力只实现一次 + 契约先行**；AI 功能须过专项评审六问，重要选型写 ADR。

## Frameworks Introduced
- **公共能力 Owner 表**: LLM 网关、配置密钥、身份权限、数据访问、Agent/工具协议、记忆、日志追踪、统一异常响应 — 各指定唯一负责人，禁止各 Agent 复制一套。
- **契约先行清单**: API 路径与错误码、工具 Schema、表字段与枚举、事件载荷、依赖方向与 Owner。
- **AI 方案评审六问**: 为何 LLM、数据边界、工具与校验、兜底、评测与成本、变更回归与回滚。
- **ADR**: 问题、候选、选择、原因、代价、复查条件 — 例：P1 轻量向量库，规模上来再评 Milvus。

## Reference Tables
| POST /api/chat 关键字段 | 说明 |
|------------------------|------|
| agent_type | customer/advisor/risk/analyst/operator |
| session_id / user_id | 会话与用户 |
| 响应 reply, source_references, tool_calls, intent, confidence | 统一包 code/message/data/trace_id |

## Code Examples
```javascript
export const mockChatResponse = {
  reply: "根据产品手册…",
  source_references: [{ title: "产品手册", score: 0.92 }],
  intent: "product_consult",
  confidence: 0.85
};
```
- **What it demonstrates**: 契约未就绪时前端 Mock 并行开发

## Worked Example
改公共契约流程: 讨论 → 更新契约文档 → 再改代码；Reviewer 检查 PR 是否同步调用方。

## Key Takeaways
1. 前端/后端/Agent 不对等等待 — Mock/Stub 解耦
2. 接口变更通知相关方；不兼容变更给迁移路径
3. Swagger 随定义更新

## Connects To
- **Ch 5**: 模块与 Phase 分工
- **Ch 7.2**: Prompt 与接口同级版本管理
