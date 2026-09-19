# Cheatsheet — AI 金融项目开发指南

## 决策规则

| 当… | 则… | 因为… |
|-----|-----|-------|
| 输出须确定（适当性/金额/权限） | 写规则代码，不用 LLM | 合规与可测试 |
| 能查库/调接口得答案 | NL2SQL/NL2API + 校验 | 稳定低成本 |
| 必须上 LLM | 兜底+黄金集+trace | 概率输出需约束 |
| 改 Prompt/知识库/模型 | 跑同一评测集，对比基线 | 防 silent 退化 |
| 阶段门禁未过 | 回退补交付物 | 避免集成爆雷 |
| 低置信/无依据 | 澄清、拒答或转人工 | 金融不能硬答 |
| 写操作 | 二次确认+幂等键 | 防重试重复下单 |
| 多 Agent 传上下文 | 只传结论+依据 ID | 防 token 爆炸 |
| 演示前 3 天 | 干净机 clone+compose≤15min | 防 -20 |
| 答辩现场出 Bug | 说明计划，不改代码 | 评分纪律 |

## 阈值与默认（须团队 P0 标定，禁止照搬文档示例）

- 检索 score 示例常写 0.7 → **以评测集标定值为准**
- Agent 步数预算示例 ~25 → 按图复杂度调整
- 端到端 P95 示例 <8s → 写入验收标准

## 文件 Owner 快查

| 冲突高发文件 | 处理 |
|--------------|------|
| requirements.txt | 合并双方依赖，排序 |
| app/api/chat.py | 接口负责人 |
| ORM/表模型 | 数据库负责人 |
| .env | 不提交，用 .env.example |

## PR 合并前 30 秒

- [ ] 对应 todo 已自测  
- [ ] pytest + ruff（教学最小 CI）  
- [ ] 无 sk-/password 硬编码  
- [ ] 改契约 → Swagger/调用方已同步  
- [ ] AI 改动 → 评测回归已跑  

## 五 Agent 与必问句（演示）

customer(RAG) · analyst(NL2SQL) · advisor(适当性) · risk · operator(NL2API+确认)

##  smells

- Prompt 越来越长但准确率降 → lost in the middle，查预算与重排  
- 评测集题目出现在 Few-shot → 指标虚高，训练/评测分离  
- 前缀含时间戳/UUID → 缓存全 miss  
- 「大家一起写」→ 无 Owner，合并冲突  
