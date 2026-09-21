# Chapter 9: 什么是「完成」（DoD）

## Core Idea
完成 ≠ 代码写完或本机可跑；DoD 清单覆盖功能、需求追溯、单测、**AI 评测回归**、Swagger、README、Docker、Review、无密钥、日志、迁移说明。

## Frameworks Introduced
- **DoD 十一项清单**: 功能正确、需求清晰、核心测试通过、AI 评测达标、Swagger 可访问、README 更新、docker-compose 可启、≥1 Review、无硬编码密钥、日志可排查、DB/配置变更有迁移回滚说明。
- **PR 前自测五步**: docker-compose → uvicorn → Swagger 测新接口 → pytest → ruff → 本地 grep 密钥（CI 扫描为准）。

## Code Examples
```bash
docker-compose up -d
uvicorn app.main:app --reload
pytest tests/ -v
ruff check app/
```

## Key Takeaways
1. DoD 是判定条件；怎么测见 Ch11，AI 效果见 Ch8，演示见 7.8
2. 敏感信息以 CI 密钥扫描为准，grep 仅辅助
3. 「在我电脑上能跑」不构成完成

## Connects To
- **Ch 6**: PR 与 Review
- **Ch 12**: 发布前 DoD 加严版
