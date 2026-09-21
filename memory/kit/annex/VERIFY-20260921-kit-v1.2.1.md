# VERIFY：project-memory-kit v1.2.1（§5 补 HANDOVER 的「顶部最后核实」）

- 日期：2026-09-21
- 关联 TODO：无（用户拍板选 A：只改 §5 那一行）
- 风险等级：LOW（改一行模板文字 + 版本号；不动任何模板行为）

## 改了什么

起因：用户指出本仓 `MEMORY.md` §0 的 HEAD 仍是 `ec15c94`、而 `HANDOVER.md` 已是 `e35eb2b`。补刷 §0 时按「还有谁在记这个事实」全库 grep，查出一个**模板缺口**：

一个项目里记「新鲜度」的地方**恰好两处**——`MEMORY.md` §0「工作分支」（当前提交）与 `HANDOVER.md` 顶部「最后核实」（最后一次核实本文件事实的提交）。

而**日常真正被读的那张表**（`templates/MEMORY.md` §5「文档资产约定」）的 HANDOVER 行只写「改完刷新**该条**『核实日期』」，**漏了顶部「最后核实」**。写对的地方在 `SKILL.md:114` 与 `templates/HANDOVER.md:10`——但两者日常都不读。**照 §5 干活的 Agent 会规律性漏刷顶部「最后核实」。**

| 动作 | 文件 |
| --- | --- |
| §5 HANDOVER 行：改完刷新「核实日期」→ 刷新**该条**「核实日期」**与顶部「最后核实」** | `templates/MEMORY.md` |
| 版本号 `1.2.0` → `1.2.1`（补句档，末位 +1）；升版示例刷新为 `1.2.1` → `1.2.2` | `SKILL.md` |
| 版本行 → `v1.2.1` | `README.md`、`templates/MEMORY.md` §5 |
| 进度戳补 v1.2.1 归因 | `references/design-20260921-dated-log-index.md` |
| **升版规则补判据**：「补句 vs 改口令」按「照文档干活的 Agent 会不会多做/少做/换做法」判；拿不准按「改口令」高报 | `SKILL.md` |
| 本仓跟版：§5 同一行、版本行、§0 交付记录、HANDOVER 版本事实 + §6 新增「记 HEAD 的两处」一行 + 顶部最后核实、**追加** ITERATION 一行、INDEX 加行、本文 | `memory/kit/{MEMORY.md,HANDOVER.md,ITERATION.md,annex/INDEX-20260921.md}` |

**顺带修的（用户本轮指出）：** `memory/kit/MEMORY.md` §0 HEAD `ec15c94` → `e35eb2b`。上一轮我刷了 HANDOVER 的「最后核实」却漏了 §0——两处都记 HEAD，我只刷了手边那处。

## 已执行

| 类型 | 命令或步骤 | 结果 |
| --- | --- | --- |
| 手工 | 全库 grep `HEAD\|工作分支\|最后核实\|rev-parse`（本仓 `memory/kit/` + kit 模板） | 确认恰两处记 HEAD；§5 行确为缺口 |
| 手工 | 四处版本号与 §5 行文字核对（仓库 claude/cursor + 安装 cursor/claude） | PASS：四处均 `kit-version: 1.2.1`、§5 行均含「顶部『最后核实』」 |
| 手工 | `git diff --no-index` 仓库两副本、两处安装 vs 各自仓库副本 | PASS：**三组均逐字一致** |
| 手工 | `python scaffold/scripts/check-memory-size.py` | PASS：退出码 0 |
| 手工 | `ITERATION.md` 追加语义核对（diff 是否只有 + 无 -） | PASS：仅新增 1 行，历史 8 行未改写 |

## 未执行

- 项：commit / push
- 原因：用户未要求
- 项：`templates/HANDOVER.md` 加「这里的 HEAD 不必等于当前 HEAD」防误报说明
- 原因：用户拍板只做 A（选 A 而非 B）。**故「两处不相等」这件事目前只写在 kit `HANDOVER.md` 的正文，未写进 HANDOVER 模板**——将来接手的人仍可能把「两处不等」误判为漏刷
- 项：把「记 HEAD 的两处」写进常驻口令（`templates/AGENTS.md` / `cursor-rule.mdc`）
- 原因：用户未选；当前只靠 §5 那行的一处补充覆盖
- 项：为 §5 那行加自动校验（「顶部最后核实」是否被漏刷）
- 原因：本次只补文字与判据，未加校验；**这是剩余风险②的具体缺口，仍待解决**

## 结论

- 需求覆盖：缺口已按 A 补上；遗漏的 §0 HEAD 已刷齐
- 旧功能是否破坏：无——只改文字与版本号，模板行为未变
- 剩余风险：① 「两处不必相等」未进 HANDOVER 模板，仍有被误判为漏刷的可能；② §5 行现在要求刷两处，但**没有校验手段**——`check-memory-size.py` 不管这个，漏刷仍不可自动发现
- 建议人工再验：`diff` 四处副本；打开 kit `SKILL.md` 顶部确认 `kit-version: 1.2.1`；决定是否 commit / push
