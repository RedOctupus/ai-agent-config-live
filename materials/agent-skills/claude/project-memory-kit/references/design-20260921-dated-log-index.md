# 设计：支持「当日索引」 + JinRong 存量收敛

> 日期 2026-09-21 · 状态：**已获用户批准**（双向改动 + 按日期日志降级为当日索引）
> **实施进度：Part 1 已实施并校验（kit `v1.1.0`）；v1.1.1 把 init 模板改名为 `templates/annex/_INDEX.md`（避免与 `INDEX-YYYYMMDD.md` 撞名）；Part 2 未开始**——用户指示先搁置 JinRong、专做 kit 迭代。
> 落地对象：`project-memory-kit`（`claude/` 与 `cursor/` 两份副本，改完 `diff -r` 逐字校验）
> 本文是 kit 的**演进设计记录**，不是操作指引——日常任务不要读它。

------

## 1. 背景

外部项目 `D:\项目\JinRong` 从 kit 早期版本 init 后长期未跟版，演化出一套分叉形态（`docs/memory/tests/`、`TEST-LOG-*`、按日期工作日志）。诊断后确认：**这不只是「没跟版」，kit 的迁移处方本身就接不住按日期日志的一半内容。**

### 1.1 证据

| 事实 | 实测 |
| --- | --- |
| JinRong 缺体量门闸脚本 | `scripts/check-memory-size.py` 不存在，§0 超配额 2.2 倍（2014 / 900 字符）从未被拦 |
| 按日期日志规模 | 5 份（`2026-09-09` ~ `2026-09-14`），其中两份 463 行 / 48KB、547 行 / 50KB |
| 日志内容构成 | 战报 ≈ 45% · **坑 / 环境事实 / 研究结论 ≈ 30%** · 裁定 ≈ 10% · 待办 ≈ 10% · 元信息 ≈ 5% |
| 改名波及面 | `docs/memory/tests` / `TEST-LOG-` / `MANUAL-CHECKLIST` 被 **49 个文件**引用 |
| `_raw` 未全忽略 | `.gitignore` 只忽略 `.../_raw/shots/`，`_raw/` 下 68 个非图片产物已入库 |
| kit 权威源路径过时 | `SKILL.md` 写 `agent-skills/...`，实际为 `materials/agent-skills/...`（裸路径不存在） |
| kit 无版本号 | `SKILL.md` / `README.md` 无 `kit-version`，项目侧无「按哪个版本建立」记录 |

### 1.2 根因：两个缺位

1. **跨任务的「当日汇总」没有位置。** `annex/VERIFY-*` 是「一任务一份」，但一天做 6~7 件事时按任务拆会产生十几份碎片文件，「今天整体发生了什么」这个视角没有载体。
2. **按日期日志的收敛处方只写了改名。** `migration.md:30` 只说「`tests/` → `annex/`、`TEST-LOG-*` → `VERIFY-`」，而日志里 30% 是坑 / 环境事实 / 研究结论，目标应是 `HANDOVER.md`——改名处方接不住，硬跑要么丢内容，要么污染 VERIFY。

------

## 2. 决策（用户已定）

| 问题 | 决策 |
| --- | --- |
| 改哪一侧 | **双向**：kit 吸收缺失形态，JinRong 收敛到新骨架 |
| 按日期日志怎么处置 | **降级为当日索引**：只留「今天做了什么 + 跳转链接」，正文全部拆到 `VERIFY` / `HANDOVER` / `ITERATION` / `TODO` |
| 顺序 | **先 Part 1（kit）后 Part 2（JinRong）**——否则 JinRong 拆分时还没有 `INDEX` 形态可用 |

------

## 3. Part 1 · kit 侧改动（4 项 + 1 处顺带修复）

### 3.1 新增当日索引模板

- 新建 `templates/annex/INDEX.md`，定义 `annex/INDEX-YYYYMMDD.md`。
- 形态：**纯索引**。一行一事 + 指针；当日定下的口径 / 未闭环也只留指针，正文归 `ITERATION.md` / `TODO.md`。
- 硬约束写进模板：**禁止贴正文**；**一天只有一件事时不建此文件**（直接写 VERIFY）。
- 在 `templates/annex/_TEMPLATE.md` 的「类型 / 前缀」表加 `INDEX` 行，并说明它与 `VERIFY` 的分工。
- `SKILL.md` 的 annex 前缀节同步。

### 3.2 `migration.md` 补「按日期工作日志」收敛处方

在 `references/migration.md` 的存量收敛节新增一步，给出**四类归位目标**：

| 日志里的内容 | 去哪里 |
| --- | --- |
| 逐任务战报（改动面 / 验证 / 突变验证 / 冒烟 PASS） | `annex/VERIFY-YYYYMMDD-短名.md`（一任务一份） |
| 坑 / 环境事实 / 研究结论 / 已排除的路 | `HANDOVER.md` §1/§2/§5/§6/§7 |
| 决策 / 口径裁定 / 用户拍板 | `ITERATION.md` |
| 下一步 / 未闭环 / 登记开口 | `TODO.md` |
| 原文件本身 | 降级为 `annex/INDEX-YYYYMMDD.md`（只留指针） |

并显式写明：**这一步必须走「先复制 → 逐条回读对照 → 确认零遗漏 → 才删原处」**（沿用该文件已有的强制顺序），因为这里要拆 1000+ 行到 4 个目标，漏一条坑或裁定就永久丢失。

### 3.3 新增项目用 `.gitignore` 片段模板

- 新建 `templates/gitignore-memory.txt`：

```text
# project-memory-kit 取证不入库
docs/memory/annex/_raw/
docs/memory/annex/*/_raw/
```

- `SKILL.md` 的 init 拷贝表加一行指向它。
- 理由：原逻辑只散在正文口语描述（「`.gitignore` 加同名路径」），JinRong 手写时因此只忽略了 `shots/`。给一份可直接追加的片段，比让人照着散文写可靠。

### 3.4 kit 版本号

- `SKILL.md` frontmatter 区加 `kit-version: 1.1.0`（首个带版本号的基线）。
- `templates/MEMORY.md` §5 文档资产表加一行：「本记忆按 kit **v1.1.0** 建立；kit 升版后按 `references/migration.md` 二、骨架升级跟版」。
- 理由：没有版本号，「该跟版」这件事永远只能靠人想起来——JinRong 停版正是这个后果。

### 3.5 顺带修：权威源路径过时

`SKILL.md` 第 156–157 行的权威源路径 `agent-skills/{claude,cursor}/project-memory-kit/` 在本仓库已不存在（仓内做过目录三分，kit 现位于 `materials/agent-skills/...`）。改为实际路径，否则按图索骥必然失败。

### 3.6 同步

两份副本（`claude/` + `cursor/`）改完执行 `diff -r` 逐字校验，范围 `SKILL.md` / `README.md` / `templates/` / `references/` / `scripts/`，排除 `_sandbox/`。

------

## 4. Part 2 · JinRong 收敛（11 步）

按 `references/migration.md`「二、骨架升级」执行。

| # | 动作 | 影响面 | 备注 |
| --- | --- | --- | --- |
| ① | 拷 `check-memory-size.py` → `scripts/` | 0 | 门闸落地，先跑一次拿基线 |
| ② | 建 `HANDOVER.md` | 新建 | 从日志的坑 / 结论搬；原引用的根 `交接文档.md` **已缺失**（见下） |
| ③ | 建 `REFERENCES.md` | 新建 | 只放地址，研究正文进 `annex/NOTE-` |
| ④ | `docs/memory/tests/` → `docs/memory/annex/` | 129 文件 | `git mv` |
| ⑤ | `TEST-LOG-*` → `VERIFY-*`；`MANUAL-CHECKLIST` → `CHECKLIST-` | 28 文件 | |
| ⑥ | **按日期日志拆分**（见附录 A） | 5 份 / 1129 行 | **最易丢内容，走强制顺序** |
| ⑦ | 引用同步（49 文件） | 49 | 含 `docs/course/` 生成物（改了可能被 build 覆盖，需确认归属） |
| ⑧ | `.gitignore` 改 `_raw` 全文忽略 | 1 | 已入库的 68 个产物需决定是否 `git rm --cached` |
| ⑨ | 补常驻口令（`AGENTS.md` + `mdc` 各 10 句） | 2 | 逐句对照 `templates/`，两处必须同时改 |
| ⑩ | `MEMORY.md` §0 压到 ≤900 字符、§3 约束拆分 | 1 | 跑门闸验证 |
| ⑪ | `TODO.md` 改形状 | 1 | 只改形状，不改事实 |

**第 ② 步的前提核实（重要 · 2026-09-21 现场核实）：**

先厘清一件事——**kit 里没有名为「交接文档」的物件**。kit 全库仅一处出现该词：`templates/HANDOVER.md` 的 H1 标题 `# 项目交接文档（必知事实）`。因此 kit 的跨阶段事实文件是 `HANDOVER.md`，不存在第二个同类概念。

JinRong 侧曾被引用为「三线合并唯一接手入口」的 `交接文档.md`（JinRong 项目根、非 kit 物件），**现场核实已不存在**：

| 检查项 | 结果 |
| --- | --- |
| 项目根文件系统 | 根 `.md` 仅 `AGENTS.md` / `README.md`，无此文件 |
| `git ls-files --error-unmatch` | 未跟踪 |
| `git log --all --diff-filter=A -- 交接文档.md` | 空——从未 add |
| `git log --all -- 交接文档.md` | 空——全历史零 commit 含此路径 |
| `.gitignore` | 第 58 行 `交接文档.md`（故从未入库） |
| 全 `D:\项目` 搜同名 | 仅 `docs/交接文档-基金转换.md`、`docs/交接文档-架构改进.md`（JinRong 自标「已废弃 · 勿读」） |

`2026-09-10.md` 记录其当时为 v3.0 / 545 行，且「两份工作区最新版**从未提交**、随时可能丢，现已完整固化」——被固化进该文件的内容，因未入库而**git 不可恢复**。

**待用户确认**：该文件是有意删除 / 迁走，还是丢失？处置方式影响第 ② 步：

| 情形 | 第 ② 步做法 |
| --- | --- |
| 仍在别处（另一机器 / 盘） | 取回，按下方边界拆分 |
| 确实丢失 | 从 5 份按日期日志 + `ITERATION.md` + `docs/` 各源文件**重建**事实（第 ⑥ 步的归位映射表即为重建输入） |
| 有意废弃 | 修掉 JinRong `AGENTS.md` 顶部的悬空指针，直接以 `HANDOVER.md` 替代 |

**边界（无论哪种情形都适用）：**

| 内容 | 去哪 | 理由 |
| --- | --- | --- |
| 环境 / 路径 / 账号位置 / 工具版本 / 研究结论 / 坑 / 已排除的路 | `HANDOVER.md` | 正是 kit §1~§7 的定义，且这类事实**该入库**、该被跟版 |
| 各线的当前状态、下一步、线级导航 | 只保留**活跃线**；已收官线的状态归档到 `annex/INDEX-*` | 线状态会变，不宜进「长期成立的事实」表 |
| 不入库的敏感内容 | **禁止**进 `HANDOVER.md` | 若确有敏感内容需本地留存，另建 gitignored 文件，并在 `HANDOVER.md` 留一行指针说明其存在与位置 |

**这条发现反向支持本设计**：`HANDOVER.md` 之所以规定入库、行内改、带「核实日期」，正是为了不让跨阶段事实只存在于一个未入库、无人校验的文件里。

------

## 5. 附录 A · 归位映射表（第 ⑥ 步实施依据）

**四个目标桶**：`VERIFY`（战报）· `HANDOVER`（坑 / 环境 / 结论）· `ITERATION`（裁定）· `TODO`（待办）。

### `2026-09-09.md`（37 行 · 架构改进线 11 项）

| 这节在讲什么 | 源 | 归位 |
| --- | --- | --- |
| 11 项改动 + 验证 + 纪律核查 | `## 完成项` / `## 纪律核查` | `VERIFY-20260909-arch-hardening.md` |
| 架构设计说明书实际文件名与引用不符 | `## 差异备注` | `HANDOVER.md` §2 |
| 第 3/4 批未动 | `## 未做` | `TODO.md` |
| commit + 510 passed 复核 | `## 提交与复核` | VERIFY |
| 遗留：七项冒烟待做、报告后可 push | 文末「遗留」 | `TODO.md` |

### `2026-09-10.md`（463 行 · 架构线收尾 + 转换线 T-8~T-13）

| 这节在讲什么 | 源 | 归位 |
| --- | --- | --- |
| 冒烟 7 项全 PASS（含口径替代留痕） | `## 二、第 1~7 项` | `VERIFY-20260910-smoke7.md` |
| 本机 key 为空 / Redis 无文档化启动方式 / `sc.exe` 被安全策略拉黑 | 第 1、5 项内 | `HANDOVER.md` §1 |
| 两处「文档与实况不符」 | `### ⚠️ 核对中发现…` | `HANDOVER.md` §6 |
| 集成测试 3 failed 是防护行为 | `### 3.1` | `HANDOVER.md` §6 |
| 演示库重灌 11 个 SQL 顺序 + 完成标志 8/7/33 | `### 3.2` | `CHECKLIST-20260910-reload-db.md` + `HANDOVER.md` §2 |
| 全量复跑 510 绿 | `### 3.3` | VERIFY |
| 回写清单 / 各节「文档回写」 | `## 四` 等 | `ITERATION.md` |
| 交接文档 = AI 接手唯一入口（JinRong 根 `交接文档.md`，**现已缺失**） | `### 6.1` | `ITERATION.md` + `HANDOVER.md` |
| **事故：`git rm` 静默抹除整个 `docs/`（复现 2 次）** | `### 6.3` | `HANDOVER.md` §6 + §7 |
| 方法论固化为 skill、MEMORY 205→70 行 | `## 七` | `ITERATION.md` + VERIFY |
| T-8~T-13 各「改码 N 处」 | 各节 | VERIFY（按任务拆 6 份） |
| 阶段 1.5 从「静默跳过」变「真跑」 | T-8 `⭐ 实质影响` | `HANDOVER.md` §5 |
| 真库脚本两条踩坑（`id_factory` / MySQL ENUM ORDER BY） | T-8 | `HANDOVER.md` §6 |
| RISK-001 单笔 vs RISK-002 当日累计 | T-8 | `HANDOVER.md` §5 |
| 各任务「执行期裁定 N 条」（共 ~13 条） | 各节 | `ITERATION.md` |
| 二次误报「远程分支不见」+ **`refs/remotes` 不落盘 7 条证据 + 绕过** | T-9 `🔴` / 深夜节 | `HANDOVER.md` §6/§7；7 条证据进 `NOTE-` |
| 展示位数契约缺位 + 联网核验 7 家管理人 | T-9 收尾 | `NOTE-20260910-display-scale.md` + `HANDOVER.md` §5 |
| 「格式契约铁律」（`str(Decimal)` 必问展示位数） | T-9 收尾 | `HANDOVER.md` §6 |
| 50 并发压测结论 + InnoDB 1213 死锁 + 退避根因 | T-13 | `HANDOVER.md` §5/§6 + `TODO.md` |
| 性能 P50 44.2 / P95 51.5 | T-13 | VERIFY |

### `2026-09-12.md`（547 行 · 转换线 T-11~T-17 + 集成测试 + 收官）

| 这节在讲什么 | 源 | 归位 |
| --- | --- | --- |
| 各任务「改动面」 | `## 一` × 7 | VERIFY × 7 |
| **联网核实长表格**（转换失效口径 / T-14 依据 / 易方达反证） | `## 二` × 3 | `NOTE-20260912-convert-facts.md` + `HANDOVER.md` §5 |
| 各任务「验证」（pytest / 真库） | `## 三` × 7 | VERIFY × 7 |
| 各任务「突变验证 N 组」 | `## 五` × 2 | VERIFY |
| 各任务「下一步」 | `## 四/七` | `TODO.md` |
| 硬编码全仓排查 + 补修 | `## 五b` | VERIFY |
| 2 项登记开口待裁定 | T-14 `## 六` | `TODO.md` |
| 时序口径裁定（撤单后确认幂等 skip） | T-15 `## 一` | `ITERATION.md` |
| 真库 FK 新坑 | T-16 `## 三` | `HANDOVER.md` §6 |
| R-12 口径裁定（NULL 不参与 A/C 判定） | T-17 `## 一` | `ITERATION.md` |
| 审核教训：独立 AI 审查抓不住外部事实断言 | 收官节 | `HANDOVER.md` §6 |
| 集成测试五步全过 + 31 紧池 / 18 性能重测 | `# 第 6 步` | VERIFY（里程碑） |
| 种子补拉 + 全套重测 | `# 种子补拉` | VERIFY |
| README 更新 + push + tag `convert-m1` + PR | `# README 更新` | VERIFY + `ITERATION.md` |

### `2026-09-13.md`（24 行 · 客户线交易收口）

| 这节在讲什么 | 源 | 归位 |
| --- | --- | --- |
| P0 鉴权 / P1 适当性 / L1 幂等 / CT6 / T1 | `## 做了什么` | `VERIFY-20260913-ct001.md`（由 `TEST-LOG-CT-001` 改造） |
| 55+ passed | `## 验证` | 同上 |
| CT-001 复跑 / B1 / T1 / CT11 / git 未 commit | `## 仍开放` | `TODO.md` |
| 记忆同步清单 | `## 记忆同步` | `ITERATION.md` |

### `2026-09-14.md`（58 行 · 一天 7 件事）

| 这节在讲什么 | 源 | 归位 |
| --- | --- | --- |
| 三缺陷修法 + 5 处测试 bug + F-β 选A | `## 做了什么` / `## 5 处…` | `VERIFY-20260914-multiturn3defects.md` |
| #4 是真产品 bug（`looks_like_trade_execute` 误判） | 表格第 4 行 | VERIFY + `HANDOVER.md` §6 |
| git 工作区大量未 commit | `## 仍开放` | `TODO.md` |
| 前端测试台**已在远程**、早期纪律已变 | 测试台节 `结论` | `HANDOVER.md` §5 |
| fetch 302 重定向 → stale ref 误判 | 测试台节 `坑` | `HANDOVER.md` §6 |
| 远程 merger 同步（BM25 + 协助申请表 + 需跑迁移脚本） | merger 节 | VERIFY + `HANDOVER.md` §2 |
| 顾问关系图读模型 / 出口 / 相机 / 灌库 | 关系图节 | VERIFY |
| 对话误要「再鉴权」 | 关系图节 | `HANDOVER.md` §6 |
| AG-001 压测 19 PASS / 1 FAIL + 3 水温问题 | 关系图节 | VERIFY |
| AG-002 两缺陷闭环（路由漏配 + `<tool_call>` 泄漏） | AG-002 节 | VERIFY |
| **AG-001 为何没抓到：已知缺口标 `pressure` + 豁免 → 测试绿产品破** | AG-002 `为何没抓到` | `HANDOVER.md` §6 |
| 全量 1321 passed / 61 failed / 23 errors 均为既有问题 | AG-002 节 | `HANDOVER.md` §5 |
| AG-002 三项未闭环 | AG-002 `未闭环` | `TODO.md` |
| 记忆同步（3 处） | 各节 | `ITERATION.md` |

------

## 6. 风险与顺序

| 风险 | 说明 | 缓解 |
| --- | --- | --- |
| 第 ⑥ 步丢内容 | 1129 行拆到 4 个目标，漏一条坑或裁定即永久丢失（`migration.md` 自述丢过一条决策条目） | 严格走「先复制 → 逐条点名回读 → 零遗漏 → 才删」；拆完跑门闸 |
| 第 ⑦ 步漏改链接 | 49 个文件含 `docs/course/` 生成物与 `.gitignore` | 改完 `git grep` 复扫 `tests/` / `TEST-LOG-` 零命中 |
| 已入库的 `_raw` 产物 | 68 个文件已在 git 里 | 第 ⑧ 步单列，`git rm --cached` 需用户确认后执行 |
| 两份副本分叉 | kit 自述分叉过一次 | 改完 `diff -r` 逐字校验 |

**顺序：Part 1 全部完成并校验后，才动 Part 2。**

------

## 7. 未纳入本次范围

| 议题 | 状态 | 说明 |
| --- | --- | --- |
| **工作线（workstream）作为 kit 一等概念** | **搁置**，本次不做；但理由已被削弱，需重估 | JinRong 的「线」（风控主线 / 基金转换线 / 架构改进线）有明确生命周期（收官、结项），与 `references/team.md` 假定的「长期存在的模块」不同。原本「搁置」的依据是「收敛靠现有 `交接文档.md` 分节 + `ITERATION.md` 已能承载」——而 `交接文档.md` **现已缺失**，即**承载线级状态的载体没了**。若第 ② 步选择「不重建」，则线级状态将无处安放，本议题从「搁置」转为**待决**；若选择重建，则维持搁置。 |
| 多人 / 多模块（`team.md` 的 `OWNERS.md` / `GLOBAL/`） | 不适用 | JinRong 单人 + 多线，不触发多模块骨架。 |
| `_raw` 已入库的 68 个文件是否 `git rm --cached` | 待用户拍板 | 见 §4 第 ⑧ 步与 §6 风险表。 |

