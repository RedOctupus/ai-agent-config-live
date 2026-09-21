# 测试日志：目录三分（脚手架 / 记忆 / 本地物料）

- 日期：2026-09-21
- 关联 TODO：已完成「目录三分」；R8
- 风险等级：MEDIUM

## 改了什么

- 文件：根目录迁到 `scaffold/`、`memory/{kit,hermes}/`、`materials/`；`scaffold/scripts/*` 路径；`README.md` / `AGENTS.md` / `.cursor/rules/project-memory.mdc` / `.gitignore`；`memory/kit/*` 路径回写
- 行为变化：同步/恢复脚本从 `scaffold/scripts/` 上两级找仓库根；Hermes 导出只写 `memory/hermes/`；kit 默认检查 `memory/kit/MEMORY.md`；`.env`、取证 `_raw`、`materials/_local/` 忽略

## 已执行

| 类型 | 命令或步骤 | 结果 |
| --- | --- | --- |
| 手工 | `python scaffold/scripts/check-memory-size.py`（仓库根） | PASS：退出码 0；MEMORY 210 行 / §0 实义 6 行·504 字符 / 最长行 179 |
| 手工 | 关键路径 Test-Path（脚本、kit MEMORY、hermes 导出、skills/agent-skills/tools/plans、`_local/.gitkeep`） | PASS：全部 OK；旧根 `docs`/`scripts`/`agent-skills`/`hermes`/`skills`/`tools`/`plans` 均 gone |
| 手工 | `git check-ignore -v` 抽样 | PASS：`memory/kit/tests/_raw/`、`materials/_local/*`、`.env` 命中忽略；`materials/_local/.gitkeep` 例外保留；`materials/hermes/.env.template` 未忽略 |
| 手工 | kit 模板副本仍含 `docs/memory/MEMORY.md` | PASS：`materials/agent-skills/cursor/project-memory-kit/scripts/check-memory-size.py` 未改 |

## 未执行

- 项：`./scaffold/scripts/restore.sh` 真恢复、`sync-skills.sh` 对本机 Hermes 实拷、双机冲突合并、Git Bash `bash -n` 语法检查
- 原因：真恢复会覆盖本机 Hermes；sync 会改 skills 树；本机默认 shell 是 PowerShell

## 结论

- 需求是否覆盖：R8 目录三分 + gitignore 已对照；R1–R7 路径已改到 `materials/` 与 `memory/kit/`
- 旧功能是否破坏：若本机 cron / 快捷方式仍调用 `./scripts/*.sh`，会找不到（README 已改成 `./scaffold/scripts/`）
- 剩余风险：未提交；`auto-sync.sh` 里 `REPO_DIR="$HOME/ai-agent-config-live"` 仍是旧克隆路径，换机需改
- 建议人工再验：打开 `README.md` Structure；本机若有定时同步，把脚本路径改到 `scaffold/scripts/`
