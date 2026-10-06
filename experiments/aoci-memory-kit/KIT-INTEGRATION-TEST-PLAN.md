# Kit → AOCI 联动测试计划（执行前定稿）

日期：2026-10-06。上一轮 [TEST-PLAN.md](TEST-PLAN.md) 只验证 AOCI 自身，**没有**验证用户真正要求的 Kit 同轮行动。本轮只在已存在的实验沙盒 `sandbox/ssss-agent/` 内改动，不改原 SSSS、Kit 权威模板、主仓 `memory/kit/`、全局 MCP/技能/配置，也不接业务服务。

## 要验证的最小契约

1. Kit 的 `docs/memory/MEMORY.md` 只加**条件式入口指针**：需要理解/修改受管源码才走根 `AGENTS.md` 的 AOCI 运行合同；纯文档/业务问答继续 Kit-only。AOCI 不替 Kit 决定需求、技术选型、验收事实。
2. 同一代码任务顺序：`MEMORY` → AOCI rules/完整 Overview（或当前版本要求的身份确认）→ 目标 Entry＋真实源码/测试 → 最小代码修改 → 离线测试 → 最终稳定态 `aoci_maintain`/必要 Entry 更新 → `verify`/`check`/Guide 对齐 → Kit §5 的 VERIFY 与 ITERATION；阶段一句话不变则 MEMORY 不添战报。
3. AOCI 发生故障或未对齐时，不能把旧地图当当前证据，也不能将本轮代码交付报告为“全部完成”；Kit 仍可凭源码/测试工作，但须标注地图待维护。

## 用例与通过条件

| ID | 动作 | 通过条件 |
| --- | --- | --- |
| K01 | 在沙盒 `MEMORY.md` 加上述唯一入口；从该文件模拟日常首读 | 指针可解析到根 AGENTS；没有复制 AOCI 手册、没有把 AOCI 当业务/选型权威；MEMORY 体量通过。 |
| K02 | 对已受管的 `review_contract.py` 做源码理解 | 通过真实 MCP 获取规则、完整 Overview／具体 Entry；源码验证 `_confidence_ok` 的有限数判断；记录服务/Index 身份。 |
| K03 | 在沙盒做行为等价的一行代码重写：`math.isnan(x) or math.isinf(x)` → `not math.isfinite(x)` | 只改该沙盒文件；不新增依赖或业务规格；独立离线测试证明常见值、NaN、±Inf 结果不变。 |
| K04 | 代码稳定后触发 AOCI 漂移与增量维护 | 改动后 `verify` 指出该文件 stale；MCP 签发仅该文件候选，模型据源码维持/修订语义并绑定 SHA；最终 `verify/check/Guide` 全部 aligned。 |
| K05 | 同轮完成 Kit 文档回写 | 沙盒新建一份 `docs/memory/annex/VERIFY-...md`，向 `ITERATION.md` 追加一行；不滥改 REQUIREMENTS/FRAMEWORK/FLOW/HANDOVER，`MEMORY` 除 K01 指针不写战报；VERIFY 引用 AOCI 校验结果和测试命令。 |
| K06 | 完成后检查不变量 | 原 SSSS 清单/哈希/Git 状态与试前完全相同；沙盒 Kit 指针有效，AOCI aligned；无业务服务或 AOCI 后台进程；主仓现有文件未被本轮改写。 |
| K07 | 负路径（只读模拟） | 模拟 MCP 命令不可用或索引不对齐时，流程能明确进入“Kit＋源码核验、AOCI 待维护”而不是默默跳过；不需要破坏正式索引。 |

**判定：** K01–K06 全过才能说“Kit 的一次代码改动联动在这个沙盒跑通”。K07 至少检查决策路径；无法进行真实新 Codex Agent Run/Attestation 时单列未覆盖，不冒充全宿主验收。此测试只证明工作流组合，不比较谁效果更好。
