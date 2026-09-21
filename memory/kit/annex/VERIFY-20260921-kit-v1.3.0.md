# VERIFY：project-memory-kit v1.3.0（§0 只留分支名）

- 日期：2026-09-21
- 关联 TODO：无（用户选优化项 1）
- 风险等级：MEDIUM（改维护口令；两份副本必须逐字一致；常驻口令两处必须同时改）

## 改了什么

用户拍板：MEMORY §0「工作分支」只留分支名，短哈希只出现在 HANDOVER 顶部「最后核实」。属「改口令」，中位 +1（`1.2.1` → `1.3.0`）。

| 动作 | 文件 |
| --- | --- |
| §0 工作分支改为只留分支名 | `templates/MEMORY.md` |
| 顶部「最后核实」下补「短哈希只写这一处」 | `templates/HANDOVER.md` |
| 去掉「刷新 §0 HEAD」；写明短哈希在 HANDOVER | `templates/AGENTS.md`、`templates/cursor-rule.mdc`、`SKILL.md` 日常维护表 |
| 版本 `1.3.0`；升版示例 `1.3.0` → `1.3.1` / `1.4.0` | `SKILL.md`、`README.md`、`templates/MEMORY.md` §5 |
| 骨架升级典型触发补 v1.3.0 例子 | `references/migration.md` |
| 进度戳补 v1.3.0 | `references/design-20260921-dated-log-index.md` |
| 本仓跟版 | `memory/kit/{MEMORY.md,HANDOVER.md,ITERATION.md,annex/INDEX-20260921.md}` · `AGENTS.md` · `.cursor/rules/project-memory.mdc` |

## 已执行

| 类型 | 命令或步骤 | 结果 |
| --- | --- | --- |
| 手工 | `python scaffold/scripts/check-memory-size.py` | PASS：退出码 0；213 行 / §0 实义 6 行·517 字符 / 最长行 179 |
| 手工 | `git diff --no-index` 仓库 claude vs cursor kit | PASS：退出码 0（仅 CRLF warning） |
| 手工 | 残留「刷新 §0 HEAD / 分支名 + HEAD / rev-parse --short HEAD」 | PASS：kit 模板、本仓 AGENTS / mdc / MEMORY 无命中 |
| 手工 | `kit-version: 1.3.0`（仓库两副本 + 本机 cursor 安装） | PASS |
| 手工 | 本仓 MEMORY §0「工作分支」 | PASS：`` `main` ``，无 `@ <sha>` |

## 未执行

- 未 commit / 未 push
- 未做优化项 3（设计文进度戳当 changelog 的裁剪）

## 结论

- 需求覆盖：一处事实一处写
- 跟版动作：老项目从 MEMORY §0 删掉 `@ <sha>`，常驻口令去掉「刷新 §0 HEAD」
