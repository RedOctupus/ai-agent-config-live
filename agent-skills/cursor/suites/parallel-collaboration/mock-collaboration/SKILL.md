---
name: mock-collaboration
description: >-
  Generates a Mock data collaboration spec so teams can develop in parallel
  without waiting for real APIs. Use when dependencies are unfinished, the user
  says mock 数据, 模拟数据, 接口还没好, 先 mock, 等服务层切换, or needs
  contract-first mock design. Phase 2 of parallel-collaboration. Requires data
  contract before mock data.
---

# Mock Collaboration（阶段 2：Mock）

生成《Mock 数据协作规范》：按数据契约先 Mock，真实接口完成后只换服务层实现。

若无数据契约，先执行 `collaboration-contract` 补齐接口/数据约定，再回到本 Skill。

## 核心原则

1. **数据契约先于 Mock** — 字段名、类型、枚举、空值、分页、错误结构先定
2. Mock 严格遵守契约，不为页面方便私自改字段名、类型或结构
3. 业务页面**不得硬编码 Mock**，须走统一数据服务层/接口层/Mock 服务
4. 真实接口完成后，**只替换服务层实现**，业务页面尽量不动
5. Mock 须覆盖：正常、空数据、加载中、无权限、报错、分页/边界值
6. 每份 Mock 须登记：对应真实接口、契约版本、负责人、切换条件
7. Mock 仅用于并行开发和测试；联调/发布前须清理、关闭或隔离
8. 未提供关键契约或数据模型 → 先列缺失信息，不猜测关键字段

## 执行流程

### 1. 收集上下文

| 上下文块 | 内容 |
| --- | --- |
| 项目需求 | 背景 |
| 技术栈 | 框架等 |
| 当前要开发的功能 | 功能与数据依赖 |
| 模块分工 | 负责人与完成状态 |
| 已有接口或数据契约 | 接口文档、字段表、类型定义 |
| 现有目录和服务层 | 接口封装、调用方式 |
| 限制条件 | 旧接口兼容、不可改模块、交付时间等 |

### 2. 阅读输出模板

读取 [templates/mock-output.md](templates/mock-output.md)，按章节生成《Mock 数据协作规范》。

### 3. 设计与交付

- 给出具体接口、目录、数据结构、接入建议，不只讲概念
- **必须输出第 5 节 Mock 登记信息**，供 `legacy-mock-cleanup` 使用
- 给出最小代码示例：开发用 Mock、联调切真实接口，页面不改
- 需要实现时，配合 `test-driven-development`

## 不适合 Mock 的场景

- 强依赖真实后端状态且无法契约化（如实时交易撮合）→ 说明原因，建议等其他方案
- 无契约的关键字段 → 先补契约，不先造 Mock
