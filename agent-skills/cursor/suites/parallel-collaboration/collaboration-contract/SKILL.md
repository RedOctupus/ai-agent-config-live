---
name: collaboration-contract
description: >-
  Generates a multi-person collaboration contract document (模块拆分, 接口契约,
  数据契约, Git 协作, 目录边界). Use when starting a new project or module,
  before parallel development, or when the user says 协作契约, 契约先行,
  定接口, 模块负责人, 目录边界, or 团队开发前约定. Phase 0 of parallel-collaboration.
---

# Collaboration Contract（阶段 0：契约先行）

生成《项目协作契约文档》，让多人可并行开发、独立测试、最后顺利集成。

需求尚未定清时，先执行 `brainstorming`，再回到本 Skill。

## 执行流程

### 1. 收集上下文

向用户索取或从仓库读取以下信息。缺失时先列清单，**不要猜测**关键技术方案：

| 上下文块 | 内容 |
| --- | --- |
| 项目需求 | 目标、功能范围 |
| 技术栈 | 框架、数据库、中间件等 |
| 团队 | 人数、角色、能力 |
| 已有代码 | 目录结构、关键模块说明 |
| 约束 | 交付时间、部署环境、必选技术 |

### 2. 阅读输出模板

读取 [templates/contract-output.md](templates/contract-output.md)，按其中章节结构生成文档。

### 3. 生成契约文档

要求：

- Markdown 格式，通俗中文
- 约定尽量给出明确示例
- 不确定内容标注「待确认」
- 优先保证模块可独立开发、独立测试、顺利集成

### 4. 交付

输出完整《项目协作契约文档》，并建议保存位置（如 `docs/collaboration-contract.md` 或项目约定的契约目录）。

提醒团队：并行开发期产生的兼容层和 Mock 须登记，供后期 `legacy-mock-cleanup` 收敛。

## 核心原则

1. 先理解需求、技术栈、人员规模和约束
2. 关键上下文缺失 → 先列补充清单，不自行猜测
3. 模块之间边界清晰：职责、不负责什么、可改目录
4. 接口契约和数据契约是 Mock 与兼容层的前置条件

## 上下文占位（用户未提供时提示填写）

```text
【项目需求】
【技术栈】
【团队人数与成员能力】
【已有代码或目录结构】
【已有约束】
```
