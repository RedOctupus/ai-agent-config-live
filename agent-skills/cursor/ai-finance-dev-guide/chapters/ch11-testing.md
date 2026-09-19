# Chapter 11: 怎么测试

## Core Idea
测试左移：每小功能完成即测；分层覆盖单测/接口/集成/E2E/AI 回归/安全/性能；测试数据分正常/边界/异常/权限/AI 专项五类且脱敏版本化。

## Frameworks Introduced
- **七层测试频率表**: 单测每次改代码；接口每次新 API；集成每 Phase；E2E P5；AI 回归随 Prompt/知识库/规则/模型变更；安全每版本；性能集成后+发布前。
- **AI 评测数据五类**: 典型问、多轮歧义、无答案、注入、工具失败。

## Code Examples
```python
def test_faq_search():
    result = search_knowledge("基金申购后多久确认?")
    assert len(result) > 0
    assert result[0]["score"] >= team_threshold  # 团队标定，非照搬 0.7
```

## Key Takeaways
1. score 阈值在评测集上标定，不为绿而下调
2. NL2SQL 测禁止 DROP/DELETE
3. 测试报告记录环境、代码/数据版本、通过率与风险

## Connects To
- **Ch 7.5**: 节点序列与故障注入
- **Ch 8**: 黄金集
