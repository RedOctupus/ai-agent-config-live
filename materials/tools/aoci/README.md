# Kit + AOCI：从本仓安装与更新

本仓保存 Kit 双权威副本和**未修改的 AOCI 官方 Windows AMD64 发布包**。当前 AOCI 为 `0.1.0-rc18`；来源、ZIP / EXE SHA-256 和 provenance 在 `manifest.json`，许可证和第三方 notices 随包保留。Kit 是 Skill；AOCI 是每个 Git 工作区单独绑定的 stdio MCP。

## 本机安装（一次命令更新三个宿主）

在本仓根目录运行，使用已有 Python 3.11+，无需额外依赖或联网下载：

```powershell
python scaffold/scripts/install-memory-tools.py verify
python scaffold/scripts/install-memory-tools.py install
python scaffold/scripts/install-memory-tools.py install --apply
```

不带 `--apply` 是预览。默认更新 Codex、Claude Code、Cursor；用 `--hosts cursor` 等可只更新指定宿主。

| 资产 | 本机位置 |
| --- | --- |
| Codex Kit | `~/.agents/skills/project-memory-kit/`（使用 Claude 权威副本） |
| Claude Code Kit | `~/.claude/skills/project-memory-kit/` |
| Cursor Kit | `~/.cursor/skills/project-memory-kit/` |
| AOCI EXE / notices | `~/.local/share/ai-agent-config/aoci/<版本>/` |
| 源仓 / 本机安装定位 | `~/.local/share/ai-agent-config/memory-tools.json` |
| 旧技能、被改配置 / 定位文件备份 | `~/.local/share/ai-agent-config/backups/` |

安装器逐文件核验双权威副本，旧 Skill 整目录备份后替换；相同内容不重复写。AOCI 先校验包与 EXE，版本目录保留旧版。MCP 和索引不会随安装动作自动建立。

## 为项目绑定 MCP

先在本仓运行以下命令，`--repo` 要写**目标 clone/worktree 的绝对 Git 根**：

```powershell
python scaffold/scripts/install-memory-tools.py configure --repo 'D:\你的项目'
python scaffold/scripts/install-memory-tools.py configure --repo 'D:\你的项目' --apply
```

默认配置三个宿主；只用 Cursor 可加 `--hosts cursor`。分别合并 `.codex/config.toml`、`.mcp.json`、`.cursor/mcp.json`，只加入 `aoci`，写本机 EXE 与目标 `--repo`，并先补 Git 忽略。其他服务器、配置与 TOML 注释保留；已跟踪的机器路径配置、链接路径或同名冲突会停止。审查同名配置后可用 `--replace-aoci` 只改 command / args，保留自定义 env 等项。

Codex 还需用户信任目标项目；Claude Code / Cursor 的 MCP 批准按宿主提示操作（Cursor CLI 可在该项目运行 `agent mcp enable aoci`）。会话未加载时刷新该项目；分别用 `codex mcp get aoci`、`claude mcp get aoci`、`agent mcp list-tools aoci` 核对。

**注册 MCP 与建图是两步。** Kit init 仍分别决定单人/多人、是否启用 AOCI。明确启用后优先读取本机定位文件，复用已安装二进制；执行当前 AOCI init / Scope / scan / Guide / 模型条目维护，正式对齐才在 MEMORY 标为已启用。每个工作区只绑定自己的根，个人地图不文本合并进全局图。原有项目不会因拉取本仓而自动创建地图。

## 后续更新

```powershell
git pull --ff-only
python scaffold/scripts/install-memory-tools.py install --component kit --apply
```

Kit 更新不改变 AOCI。仓内发布包版本发生变化时，先按 Kit README 的「AOCI 升级清单」确认目标版本、冻结事务/备份并完成隔离回归，再执行：

```powershell
python scaffold/scripts/install-memory-tools.py install --component aoci --upgrade-aoci --apply
python scaffold/scripts/install-memory-tools.py configure --repo 'D:\已启用项目' --replace-aoci --apply
```

逐个受影响工作区/宿主验收新进程版本与 Verify / Check / Guide；旧版本目录仍在，未切换的项目继续用旧版。回滚恢复备份中的原配置或其旧二进制路径，再按官方回滚步骤复验。拉取只取得文件，安装/切换由显式命令完成；不需 init 时再到 AOCI GitHub 下载。

维护者更新发布包：先确认版本并核验官方 release / SHA / provenance，再更新 ZIP、许可证 notices、签名文件与 manifest；不要自行改包或只改版本号。新平台另加经过验证的包；当前没有捆绑 Linux/macOS。

官方指针：[发布版](https://github.com/aoci-spec/aoci-code/releases/tag/v0.1.0-rc18) · [宿主接入](https://github.com/aoci-spec/aoci-code/blob/v0.1.0-rc18/docs/agent-integrations.md) · [升级](https://github.com/aoci-spec/aoci-code/blob/main/docs/upgrading.md) · [回滚](https://github.com/aoci-spec/aoci-code/blob/main/docs/rollback.md) · [许可](https://github.com/aoci-spec/aoci-code/blob/v0.1.0-rc18/LICENSE)。执行时核对所选版本的文档。
