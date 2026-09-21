# Chapter 12: 发布、验收与版本管理（建议）

## Core Idea
区分 dev/test/prod（教学可合并 test）；发布前在 DoD 上加严 Prompt/知识库版本记录；通过 PR 合 main 打 Tag；发布后立即验证与回滚预案。

## Frameworks Introduced
- **环境三态**: 开发/预发布/生产 — 配置环境变量，禁硬编码密钥。
- **发布前四项**: 验收通过、迁移与 Prompt/知识库版本记录、监控回滚可用、负责人明确。
- **仓库最小树**: README、requirements、docker-compose、.env.example、app、tests、docs(表设计/API/架构/AI评测/发布回滚)。
- **Tag 发布**: develop→main PR 通过后 `git tag v1.0.0` 推送；已发布 Tag 不移动，修复走新 PR。

## Key Takeaways
1. 不提交 .env、__pycache__、大数据集
2. README 须能让他人 15 分钟内跑起（与 7.8 一致）
3. 资金/越权/核心接口/AI 指标骤降 → 停发或回滚

## Connects To
- **Ch 13**: docker-compose 启动
- **Ch 9**: DoD
