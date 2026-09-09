---
name: compatibility-layer
description: >-
  Designs a compatibility/adapter layer to extend another module without editing
  its core code. Use when the user needs to use or change someone else's module,
  wants to avoid merge conflicts, or mentions 兼容层, 适配层, legacy, 桥接,
  包装层, or 不直接改别人代码. Phase 1 of parallel-collaboration.
---

# Compatibility Layer（阶段 1：兼容层）

设计《兼容层协作方案》：在模块边界新增包装/适配/桥接代码，减少直接修改他人核心代码带来的冲突。

## 核心原则

1. **未经模块负责人确认，不直接修改他人核心业务代码**
2. 现有模块无法满足需求时，优先在边界新增包装、适配、扩展或桥接
3. 兼容层是临时手段，不允许长期堆积
4. 登录鉴权、金额计算、数据库核心结构、全局配置、项目入口等高风险区 — **禁止擅自加兼容逻辑绕开**，须提出统一修改方案
5. 未提供关键代码、接口或数据结构 → 先说明缺什么，不猜测
6. 判断「他人模块」前，先查负责人表、CODEOWNERS 或协作契约
7. Git 最后修改者 ≠ 模块负责人；不一致时标注「待确认」

## 执行流程

### 1. 收集上下文

| 上下文块 | 内容 |
| --- | --- |
| 项目需求 | 背景与目标 |
| 技术栈 | 框架、语言等 |
| 当前改动目标 | 要新增或修改什么 |
| 现有模块与代码 | 相关目录、接口、数据结构、关键代码 |
| 模块负责人 | 各模块归属；无则写「暂未分配」 |
| 限制条件 | 不可改的模块、交付时间、旧接口兼容等 |

### 2. 确认代码归属

按模板第 4 节执行归属确认。需要时运行：

```bash
git blame -L 起始行,结束行 文件路径
git log --follow -- 文件路径
git log -L :函数名:文件路径
```

### 3. 阅读输出模板

读取 [templates/compat-output.md](templates/compat-output.md)，按章节生成《兼容层协作方案》。

### 4. 评估与交付

- 结合实际上下文给出具体方案，不只讲概念
- 若兼容层会让结构变复杂、重复或有安全风险 → 明确指出，给出替代方案
- **必须输出第 6 节登记信息**，供后期 `legacy-mock-cleanup` 使用
- 需要写代码时，配合 `test-driven-development`

## 不适合用兼容层时

- 必须改高风险区核心逻辑 → 与负责人协调统一修改，不走绕路兼容
- 兼容层已成稳定公共能力 → 建议重构为正式模块，而非继续堆叠
