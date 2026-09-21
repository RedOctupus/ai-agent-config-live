# 需求拆解（对照开发）

> 下列条目从 README / `materials/agent-skills/README.md` / 仓内已有目录**归纳**，不是当次【需求讨论】会议纪要。机主未逐条口头确认「本轮范围」；发现冲突以那两份 README 为准。

------

## 本轮范围

- **目的（与 MEMORY 一致的一句话）：** 技能与配置能从 GitHub 私仓恢复，且 Cursor 技能只推不自动拉。
- **明确不做：** 不做多人协作产品、不做对外 API、不把密钥提交进 git、不自动把远端技能安装到本机、不备份 Cursor 内置 `skills-cursor`。

------

## 条目

| ID | 需求（用户可感知的行为） | 验收对照 | 状态 | TODO |
| --- | --- | --- | --- | --- |
| R1 | Hermes 技能可从 `materials/skills/` 按分类找回（含 `manifest.md` 索引） | 存在 `materials/skills/manifest.md` 且各分类下有 `SKILL.md` | 已对照 |  |
| R2 | Cursor 个人技能备份在 `materials/agent-skills/cursor/`（平铺 + `suites/`） | `materials/agent-skills/README.md` 清单与目录能对上 | 已对照 |  |
| R3 | 默认不会把仓库技能拷回 `~/.cursor/skills` 或替本机注册 | 规则写在 README；无自动 install hook | 已对照 |  |
| R4 | 灾难恢复有书面步骤：clone → restore → 填密钥 → doctor | `README.md` Quick Recovery + `scaffold/scripts/restore.sh` | 已对照 |  |
| R5 | 仓内不出现 API key 正文 | 仅 `materials/hermes/.env.template`；无提交的 `.env` | 已对照 |  |
| R6 | project-memory-kit 在本仓维护 Cursor/Claude 两份 | `materials/agent-skills/cursor/project-memory-kit` 与 `.../claude/project-memory-kit` | 已对照 |  |
| R7 | 本仓自身可用 kit 交接（本仓路径是 `memory/kit/`） | 存在 MEMORY 及源文件，`python scaffold/scripts/check-memory-size.py` 退出 0 | 已对照 | 见 tests/20260921-init-memory-kit.md |
| R8 | 脚手架、记忆、本地物料分开放；密钥/取证/本机临时夹进 gitignore | 根目录仅入口文档；三层目录存在；`.gitignore` 含 `.env`、`_raw`、`materials/_local` | 已对照 | 见 tests/20260921-classify-repo-layout.md |

状态：`未做` → `开发中` → `已对照`。
