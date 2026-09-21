---
name: parallel-collaboration
description: >-
  Routes multi-person parallel development (vibecoding) through contract-first,
  compatibility-layer, and mock workflows. Use when the user mentions 多人并行开发,
  减少冲突, 契约先行, 兼容层, legacy, mock 数据, 并行协作, 团队协作契约,
  or asks which parallel-development phase to use. Read this hub first, then
  invoke the matching phase skill.
---

# Parallel Collaboration（总控）

多人并行开发的总入口。先判断当前阶段，再转到对应子 Skill；不要在一个对话里混跑多个阶段。

## 三条思想

详见 [principles.md](principles.md)。摘要：

1. **契约先行** — 接口、数据、目录边界先定，不等别人写完
2. **兼容层** — 不直接改他人核心代码，在边界加适配层
3. **Mock** — 按契约先 Mock，后期只换服务层

## 阶段路由

根据用户意图选择**一个**子 Skill，读完并执行：

| 阶段 | 子 Skill | 典型触发 |
| --- | --- | --- |
| 0 定契约 | `collaboration-contract` | 新项目、新模块、团队开发前定规矩 |
| 1 兼容层 | `compatibility-layer` | 要用/扩展别人模块，但不想直接改他的代码 |
| 2 Mock | `mock-collaboration` | 等别人接口/数据，想先按契约 Mock 继续开发 |
| 3 清理 | `legacy-mock-cleanup` | 联调、稳定、发布前，收掉兼容层和 Mock |

用户未说明阶段时，按此顺序判断：

1. 是否已有协作契约？没有 → 阶段 0
2. 是否在等依赖接口/数据？是 → 阶段 2
3. 是否需要动他人模块代码？是 → 阶段 1
4. 是否进入联调/发布收敛？是 → 阶段 3

仍不确定时，向用户确认当前阶段，不要猜测后执行。

## 执行规则

1. **一次只跑一个阶段** — 契约、兼容层、Mock、清理各有独立 Skill
2. **子 Skill 负责产出** — 本 Skill 只做路由与原则，不替代子 Skill 的输出格式
3. **登记可追溯** — 阶段 1、2 产生的兼容层/Mock 必须登记，供阶段 3 清理
4. **缺失信息先问** — 各子 Skill 要求的关键上下文未提供时，先列清单，不编造

## 子 Skill 路径

| Skill | 目录 |
| --- | --- |
| collaboration-contract | `~/.cursor/skills/collaboration-contract/` |
| compatibility-layer | `~/.cursor/skills/compatibility-layer/` |
| mock-collaboration | `~/.cursor/skills/mock-collaboration/` |
| legacy-mock-cleanup | `~/.cursor/skills/legacy-mock-cleanup/` |

## 快速示例

**用户**：「7 个人从零做一个项目，怎么减少冲突？」
→ 读 `principles.md`，引导阶段 0，执行 `collaboration-contract`

**用户**：「我要用 auth 模块但不想改它的核心代码」
→ 执行 `compatibility-layer`

**用户**：「后端接口还没好，前端怎么先开发？」
→ 执行 `mock-collaboration`

**用户**：「要上线了，把临时兼容层和 Mock 清掉」
→ 执行 `legacy-mock-cleanup`
