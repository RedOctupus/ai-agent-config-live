# Chapter 3: 立项、需求与 MVP

## Core Idea
立项一页纸定业务问题、用户、目标、**可度量**成功指标与边界；需求按角色→痛点→场景→功能→验收走，MVP 用 MoSCoW 四档，需求全程可追踪到 PR 与测试。

## Frameworks Introduced
- **场景卡八字段**: 名称、角色、前置、输入、系统处理、正常输出、异常兜底、验收标准 — 每核心场景至少一张。
- **MoSCoW 四档**: Must/Should/Could/Won't — Won't 写入清单防 scope creep。
- **需求追踪链**: REQ 编号 → 设计 → 任务/PR → 测试用例 → 发布版本。

## Reference Tables
验收示例（Given-When-Then）:
```text
Given 客户 R2、产品 R4
When 投顾 Agent 推荐该产品
Then 拦截、说明原因、记录 trace_id 与规则编号
```

## Worked Example
成功指标改写: 「RAG 效果好」→「固定评测集引用正确率 ≥ 团队 P0 标定阈值，无依据问题拒答」。

## Anti-patterns
- **口头需求插队**: 未评估就开发
- **照搬示例阈值**: 0.7、90% 等须团队在基线上自定

## Key Takeaways
1. 成功指标必须可验收、可测试
2. 变更须记录原因、影响、负责人与是否本期
3. Milvus/Neo4j/GraphRAG 是候选非必选，按数据规模选型

## Connects To
- **Ch 8**: 黄金测试集在需求确认后建立
- **Ch 11**: GWT 验收与 pytest
