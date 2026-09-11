---
name: legacy-mock-cleanup
description: >-
  Plans removal of temporary compatibility layers, adapters, and dev-time Mock
  data before integration or release. Use when entering 联调, 发布前, 清理兼容层,
  消除 mock, 收敛临时代码, or replacing mock with real APIs. Phase 3 of
  parallel-collaboration. Run verification-before-completion before claiming done.
---

# Legacy & Mock Cleanup（阶段 3：清理收敛）

生成《兼容层与 Mock 数据清理方案》：在不破坏现有功能的前提下，逐步替换临时兼容层和 Mock，完成收敛。

清理前须确认真实接口和真实数据可用；每批清理后执行 `verification-before-completion`。

## 核心原则

1. **真实接口/数据可用后再删** — 不为清代码影响未完成业务
2. 先梳理依赖和调用范围 — **禁止批量删除**
3. 小范围、可验证、分批清理 — 每批跑测试和联调
4. 业务页面最终只依赖正式服务层，不留散落 Mock 或隐式兼容
5. 兼容层已成稳定公共能力 → 评估后重构为正式模块，不机械删除
6. 登录鉴权、金额、数据库核心结构、全局配置、入口等高风险区 — 单独说明影响和回滚
7. 关键代码、接口状态、测试结果未提供 → 先列缺失信息，不猜测后删

## 执行流程

### 1. 收集上下文

| 上下文块 | 内容 |
| --- | --- |
| 项目目标与当前阶段 | 功能、联调/发布阶段 |
| 技术栈 | 框架等 |
| 兼容层清单 | 登记信息、目录、关键代码 |
| Mock 清单 | Mock 数据/服务/开关、使用位置 |
| 真实接口状态 | 已完成项、契约、未完成项 |
| 测试与联调 | 已有测试、已验证场景、已知问题 |
| 限制条件 | 不能停服、旧版本兼容、发布时间等 |

在代码库中搜索兼容层/Mock 痕迹（如 `mock`、`adapter`、`legacy`、`compat`、`fixture` 开关），与登记信息交叉核对。

### 2. 清理准备检查

按模板第 1 节判断是否满足开始条件。不满足 → 列出前置条件和负责人，**不执行删除**。

### 3. 阅读输出模板

读取 [templates/cleanup-output.md](templates/cleanup-output.md)，生成完整清理方案。

### 4. 分批执行（若用户要求落地改代码）

- 按模板第 4 节从低风险到高风险排序
- 每批：改代码 → 跑相关测试 → 联调验证 → 再进下一批
- 对无法安全删除的项：说明原因和下一步，不强行删除
- 最高优先级：**不影响现有功能、可回滚、可验证**

### 5. 验收

输出第 8 节最终交付清单；声称完成前必须跑过相关测试并引用结果。

## 与其他 Skill 的衔接

| 时机 | Skill |
| --- | --- |
| 清理前验证 | `verification-before-completion` |
| 重构后合并 | `finishing-a-development-branch` |
| 登记信息来源 | 阶段 1 `compatibility-layer`、阶段 2 `mock-collaboration` |
