# Chapter 6: Git 分支与合并流程

## Core Idea
简化 Git Flow：feature → develop → PR+Review → main（演示/Tag）；禁止直推 main/develop，commit 规范与 PR 模板强制自测与影响面说明。

## Frameworks Introduced
- **分支铁律**: 从 develop 开 feature；合并仅经 PR；main 随时可演示。
- **Commit 类型**: feat/fix/docs/refactor/test/chore — `<type>: <描述>`。
- **PR 模板四块**: 改动内容、影响范围、自测清单、截图（前端）。
- **Review 七项**: 需求对应、逻辑、安全、规范、单测、他人影响、公共契约同步。
- **教学项目 CI 最小版**: 不做完整流水线，但 ruff + pytest + 密钥自查须在本地跑通并写入 PR（见 6.7 范围说明）。

## Code Examples
```bash
git checkout develop && git pull origin develop
git checkout -b feature/rag-knowledge
git add app/api/knowledge.py
git commit -m "feat: 新增RAG知识检索接口"
git push origin feature/rag-knowledge
```

## Worked Example
Reviewer 拒绝合并: CI/单测未过、硬编码 sk-、改契约未更新 Swagger — 补后再 Request review。

## Key Takeaways
1. 每次提交对应 todo 一项已完成且自测过
2. 受保护分支禁 force push，至少一名 Reviewer
3. 短项目可用受保护 main + 短 feature，但团队内不混用策略

## Connects To
- **Ch 10**: 冲突处理
- **Ch 12**: develop→main 发布 PR 与 Tag
