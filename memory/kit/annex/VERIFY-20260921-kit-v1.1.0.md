# VERIFY：project-memory-kit v1.1.0（当日索引 + 存量收敛处方 + 版本号）

- 日期：2026-09-21
- 关联 TODO：无（用户直接指派：「集中注意力把 Kit 迭代一下」）
- 风险等级：MEDIUM（改的是**本仓权威源**，两份副本必须逐字一致）

## 改了什么

起因：外部项目 JinRong 的记忆形态与 kit 骨架分叉，诊断后发现 kit 有两处缺位——①「跨任务当日汇总」无载体；② 存量收敛处方（`migration.md:30`）只给了 `tests/` → `annex/`、`TEST-LOG-*` → `VERIFY-` 两条改名，接不住按日期工作日志里约 30% 的「坑 / 环境事实 / 研究结论」。设计已获用户批准（见 `references/design-20260921-dated-log-index.md`）。

| 动作 | 文件 |
| --- | --- |
| 新增当日索引模板（一行一事 + 指针，禁贴正文；一天一事不建） | `templates/annex/INDEX.md` |
| 新增取证忽略片段（供项目追加到 `.gitignore`，非覆盖） | `templates/gitignore-memory.txt` |
| 存量收敛补「按日期工作日志」处方：四类归位表 + 先建 `HANDOVER` 再拆 + 强制顺序 | `references/migration.md` |
| 骨架升级节补「先比对 kit 版本号」；建缺文件加 `annex/INDEX.md` 与 gitignore 片段 | `references/migration.md` |
| kit 版本号 `v1.1.0` + 升版规则；权威源路径补 `materials/` 前缀 | `SKILL.md`、`README.md` |
| 登记 `INDEX`：init 拷贝表、annex 前缀表、日常维护表、`_TEMPLATE.md`、`README` 文档表 | `SKILL.md`、`README.md`、`templates/annex/_TEMPLATE.md` |
| 常驻口令补 INDEX 句（两处必须同时改） | `templates/AGENTS.md`、`templates/cursor-rule.mdc` |
| MEMORY 模板 §5 记录「按 kit v1.1.0 建立」+ INDEX 行 | `templates/MEMORY.md` |
| 本仓自身记忆同步（本仓也是 kit 用户）：§5 与阅读策略补 INDEX、`annex/_TEMPLATE.md` 与 `annex/INDEX.md` 就位、常驻口令两处补 INDEX 句、§0 刷新 HEAD 与交付记录、HANDOVER 补 kit 版本 | `memory/kit/{MEMORY.md,annex/_TEMPLATE.md,annex/INDEX.md,HANDOVER.md,ITERATION.md}` · 本仓 `AGENTS.md` · `.cursor/rules/project-memory.mdc` |

**设计文档：** `references/design-20260921-dated-log-index.md`（含 Part 2「JinRong 收敛 11 步」与逐节归位映射表；**Part 2 未实施**）

## 已执行

| 类型 | 命令或步骤 | 结果 |
| --- | --- | --- |
| 手工 | `python materials\agent-skills\cursor\project-memory-kit\scripts\check-memory-size.py …\templates\MEMORY.md` | PASS：退出码 0；221 行 / §0 实义 6 行·317 字符 / 最长行 217 |
| 手工 | `python scaffold\scripts\check-memory-size.py`（本仓，终值） | PASS：退出码 0；211 行 / §0 实义 6 行·572 字符 / 最长行 179 |
| 手工 | `git diff --no-index claude\project-memory-kit cursor\project-memory-kit` | PASS：**逐字一致（无差异）**；逐次镜像后各复核一次 |
| 手工 | 残留裸 `agent-skills/` 路径扫描（`SKILL.md` + `README.md`） | PASS：仅剩新写反例说明「按 `agent-skills/...` 找会落空」两处，属有意保留 |
| 手工 | 常驻口令 INDEX 句核对（kit `templates/AGENTS.md` · `cursor-rule.mdc`，本仓 `AGENTS.md` · `project-memory.mdc`） | PASS：四处均命中 `INDEX-YYYYMMDD` |
| 手工 | 新增文件落地核对（kit `templates/annex/INDEX.md`、`templates/gitignore-memory.txt`；本仓 `memory/kit/annex/INDEX.md`） | PASS：均存在 |
| 手工 | 本仓 `.gitignore` 取证忽略覆盖（第 29–32 行） | PASS：`docs/memory/annex/_raw/`、`docs/memory/annex/*/_raw/`、`memory/kit/annex/_raw/`、`memory/kit/annex/*/_raw/` 四条已在 |

## 已执行（续）· 本机安装位置同步

用户显式指定后执行。本仓 MEMORY §3 禁止的是「**静默**拷回 `~/.cursor/skills`」——本次为**显式指定**，不属静默。

| 类型 | 命令或步骤 | 结果 |
| --- | --- | --- |
| 手工 | 备份旧安装 → `%TEMP%\pmk-install-backup-20260921\{cursor,claude}` | OK：26 / 21 个文件 |
| 手工 | `robocopy <repo-cursor> <inst-cursor> /MIR` | OK：29 文件，13 复制 / 16 跳过 / 0 失败 |
| 手工 | `robocopy <repo-claude> <inst-claude> /MIR` | OK：29 文件，29 复制 / 0 失败；**清掉陈旧 `templates\tests\`**（annex 改名前的残留） |
| 手工 | `git diff --no-index` 仓库 vs 两处安装（各一次） | PASS：**两处均逐字一致** |
| 手工 | 版本标志物与陈旧目录核对 | PASS：两处 `SKILL.md:12` 命中 `v1.1.0`；`templates\tests\` 均 False |

同步前两处安装位置**版本并不相同**：Cursor 那份停在「annex 已改名、但没有 v1.1.0」；Claude 那份更旧，仍留 `templates\tests\_TEMPLATE.md`，且缺 `HANDOVER.md` / `REFERENCES.md`。

## 未执行

- 项：push 到远端
- 原因：未提交、未推送（本仓规矩：确认后由用户决定）
- 项：Part 2（JinRong 收敛）全部 11 步
- 原因：用户指示先搁置 JinRong，专做 kit

## 结论

- 需求是否覆盖：kit 两处缺位（当日汇总无载体、按日期日志收敛无处方）已补；版本号机制已加，用于判断项目是否该跟版
- 旧功能是否破坏：`INDEX` 为新增、`templates/` 其余文件仅补行；`_raw` 忽略片段是「追加」语义，不覆盖项目既有 `.gitignore`
- 剩余风险：① 两处本机安装位置**此前版本并不一致**（Claude 那份更旧），说明 kit 的「两份副本保持一致」只被落实在**仓库**里、没覆盖**安装位置**——本次已补齐并逐字校验，但**这条规矩本身仍没有机制保障**，下次改 kit 还会重演；② 权威源路径此前写错（缺 `materials/` 前缀），**说明按旧文档操作会直接落空**——若有历史会话照旧路径找过 kit，其结论不可信；③ `templates/AGENTS.md` 的 INDEX 句属 spec 未列的范围外补充
- 建议人工再验：`diff` 两份副本；打开 `SKILL.md` 顶部确认 `v1.1.0`；把 kit 同步到本机安装位置后再开新会话
