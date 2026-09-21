---
name: ai-finance-dev-guide
description: "Knowledge base from \"AI金融项目开发指南（企业流程版）\" (智能财富管家教学项目). Use when applying enterprise AI delivery for finance/education teams: MVP, contracts, five Agents, RAG/NL2SQL,评测基线, Git/DoD, demo readiness, or referencing chapter 零–十五."
---

<!-- argument-hint: [topic, e.g. DoD, 适当性, P1, trace_id, or ch07] -->

# AI金融项目开发指南（企业流程版）
**Author**: 课程工程化指南（智能财富管家） | **Words**: ~3.4K | **Chapters**: 16 (零–十五) | **Generated**: 2026-09-19

## How to Use This Skill

- **Without arguments** — load core frameworks below for AI 项目排期、契约、评测与答辩
- **With a topic** — e.g. `DoD`, `MoSCoW`, `前缀缓存`, `失败实验日志`; I read the matching chapter
- **With chapter** — e.g. `ch07` for AI 特有工程方法
- **Browse** — ask "有哪些章节" for the index

When your question is not in Core Frameworks, I load the relevant `chapters/` file first.

---

## Core Frameworks & Mental Models

### AI 项目七维 + 三条闭环
Prefer **评测+版本化** over「调通 API 即上线」。输出是概率性的；核心资产 = 代码 + 数据 + **Prompt + 知识库 + 评测集**；最危险失败是**看起来对**。必须设计：低置信澄清、无依据拒答、工具降级、转人工。成本 = 调用量 × Token × 重试；改 Prompt/知识库/模型 **必回归同一黄金集**。并行跑 **知识闭环**（文档有效期/更新）、**评测闭环**（基线→回归）、**反馈闭环**（点踩→归类→回灌评测集，不只改 Prompt）。

### 九阶段与三道门禁
Use **交付物+通过条件** when 团队文档很多但集成仍爆雷。阶段 1–3 定义、4–6 构建、7–9 验证运行。三道门禁：需求可开发可测试；功能+**AI 指标**达标；可部署/可观测/可回滚。未通过 → 回退补产出。映射本项目：**P0**=立项需求MVP+契约基线；**P1–P4**=开发；**P4–P5**=测试评测；**P5**=发布答辩。运行问题须回流需求（虚线不可断）。

### 契约先行与五 Agent
**公共能力只实现一次**（LLM 网关、权限、记忆、trace、统一错误格式），各指定 Owner。并行前锁定：`POST /api/chat` 字段、工具 Schema、表枚举、事件、依赖方向。前端用 Mock 不等后端。统一五 Agent：`customer` / `advisor` / `risk` / `analyst` / `operator`；适当性/金额/权限 **确定性代码**，模型做意图、话术、归纳、SQL/参数生成。AI 方案评审六问：为何 LLM、数据边界、工具校验、兜底、评测成本、回归回滚。

### MVP 与可追踪需求
MoSCoW：**Must** 闭环优先。场景卡覆盖异常兜底与验收。成功指标要可测（禁「效果不错」）。REQ 编号链到 PR 与测试。Given-When-Then 例：R2 客户 + R4 产品 → 推荐必须拦截并记 trace_id。

### 分工：先模块后 Agent
P1 基础设施+RAG+客服；勿第一周写完五 Agent。3–7 人按角色池合并，**公共 Owner 不可空**。任务 ≤1 天；个人 todo 0.5–2h 一步，一步一 commit。

### Git / DoD / 测试最小集
feature → develop → PR + Review → main。Commit：`feat|fix|docs|…`。教学项目：**ruff + pytest + 密钥自查** 本地跑通写进 PR（完整 CI 平台为范围外）。DoD 含 AI 评测回归、Swagger、docker-compose、Review、无密钥。

### AI 工程「关进笼子」
**LLM 决策树**：确定→规则；可查→NL2SQL/API；否则 LLM+兜底+评测。**Prompt** 外置 `app/prompts/`，改=改代码+PR+回归。**记忆**：短/中/长分层；重排+token 预算；跨 Agent 传结论+依据 ID。**前缀缓存**：稳定放前，检索片段按固定 key 排序；缓存键含模型/Prompt/知识库/工具版本；**写操作不缓存**。**测试**：断言节点序列、工具 Schema、故障（超时/空结果）；防死循环：步数预算、重复状态指纹。**AI 写代码**：不交契约/风控/金额/评测阈值；四底线：讲得清、跑得动、有测试、无幻觉库。**演示 7.8**：T-3 新机 15min 拉起；T-1 视频；必问句清单；现场**不改代码**（-20 防线）。

### 评测、安全、金融底线
P0 建**黄金测试集**与阈值，禁止事后降标。工具参数服务端 Schema 校验；写操作二次确认+幂等键；最大步数。数据最小化脱敏；trace 含版本与检索片段。冲突时**风控从严**；无依据拒答；模型输出非合规结论。

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch00](chapters/ch00-ai-vs-traditional.md) | 零、AI vs 普通项目 | 七维差异, 三条闭环 |
| [ch01](chapters/ch01-docs-first.md) | 一、先看文档 | 五 Agent, 文档优先级 |
| [ch02](chapters/ch02-nine-stage-flow.md) | 二、九阶段总流程 | 门禁, P0–P5 映射 |
| [ch03](chapters/ch03-mvp-requirements.md) | 三、立项与 MVP | 场景卡, MoSCoW, GWT |
| [ch04](chapters/ch04-design-contracts.md) | 四、设计与契约 | 公共 Owner, AI 评审六问, ADR |
| [ch05](chapters/ch05-modules-wbs.md) | 五、模块与任务 | P0–P5, todo 小步提交 |
| [ch06](chapters/ch06-git-pr.md) | 六、Git 与 PR | Git Flow, Review, 教学 CI 最小版 |
| [ch07](chapters/ch07-ai-engineering.md) | 七、AI 工程方法 | LLM 树, Prompt 生命周期, 演示预案 |
| [ch08](chapters/ch08-eval-security.md) | 八、评测与安全 | 黄金集, 工具安全, 金融底线 |
| [ch09](chapters/ch09-dod.md) | 九、DoD | 完成清单, PR 前自测 |
| [ch10](chapters/ch10-merge-conflicts.md) | 十、合并冲突 | 文件 Owner |
| [ch11](chapters/ch11-testing.md) | 十一、测试 | 七层测试, AI 数据五类 |
| [ch12](chapters/ch12-release.md) | 十二、发布 | Tag, 环境, 回滚 |
| [ch13](chapters/ch13-docker-env.md) | 十三、Docker | compose 必做 |
| [ch14](chapters/ch14-ops-feedback.md) | 十四、监控反馈 | 六维指标, 14.2 闭环 |
| [ch15](chapters/ch15-faq.md) | 十五、FAQ | 进度/合并/答辩/加分项 |

## Topic Index

- **ADR** → ch04
- **Agent 五类型** → ch01, ch04
- **DoD** → ch09
- **Git / PR** → ch06, ch10
- **LLM 决策树** → ch07
- **MoSCoW / MVP** → ch03
- **P0–P5** → ch05, ch02
- **Prompt 版本化** → ch07, ch08
- **RAG / 评测集** → ch08, ch11
- **trace_id** → ch04, ch08, ch14
- **三条闭环** → ch00, ch14
- **适当性** → ch03, ch07, ch08
- **演示预案 / -20** → ch07, ch13, ch15
- **失败实验日志** → ch07
- **docker-compose** → ch13, ch09

## Supporting Files

- [glossary.md](glossary.md) — 术语
- [patterns.md](patterns.md) — 可复用模式
- [cheatsheet.md](cheatsheet.md) — 决策规则与 PR 快查

---

## Scope & Limits

Covers the guide's process and methods only—not live repo code. Source: course/internal teaching doc; synthesized summaries, not full text. Combine with project repos for implementation. Embedded asset image paths in the original MD are not bundled in this skill.
