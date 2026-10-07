# VERIFY：家里台式机安装 Kit v1.7.1，并为 Codex 注册控制器

- 日期：2026-10-07
- 关联 TODO：无（用户口头：同步仓库，安装新 kit，给 Codex 注册新技能和 MCP）
- 风险等级：LOW

## 改了什么

- 本机 `main` 从 `4ff2ca4` 快进到 `f4e3a7f`，与 `origin/main` 一致。
- `python scaffold/scripts/install-memory-tools.py install --component kit --apply`：Cursor、Claude、`~/.agents/skills` 的 project-memory-kit 换成 **v1.7.1**，各 31 个文件与仓内权威副本逐字一致。
- 这台机器的 Codex 技能根在 `~/.codex/skills`。官方安装器只写 `~/.agents/skills`，所以把旧的 v1.6.0 整目录挪到 `~/.local/share/ai-agent-config/backups/codex-skills-project-memory-kit-20261007230713`，再镜像 v1.7.1。
- `python scaffold/scripts/install-cursor-controller.py install --apply`：技能装到 `~/.codex/skills/cursor-cli-controller`，私有环境里的 MCP SDK 为 **2.3.0**。
- `configure --apply`：在 `~/.codex/config.toml` 追加 `[mcp_servers.cursor-controller]`。原有 `node_repl` 表还在。配置备份在同目录 `config.toml.cursor-controller-20261007151332588213.bak`。
- 未安装 AOCI，未改本仓项目级 MCP 配置。

## 已执行

| 类型 | 命令或步骤 | 结果 |
| --- | --- | --- |
| 手工 | `git pull --ff-only origin main` | PASS：`f4e3a7f` |
| 手工 | kit 安装器 `--component kit --apply`，再对三份安装树做 `filecmp` | PASS：各 31 文件，无只在一侧、无内容差；`kit-version` 为 `1.7.1` |
| 手工 | 控制器 `verify`，再 `install --apply` | PASS：来源 21 文件哈希通过；安装退出码 0 |
| 手工 | 私有环境 `importlib.metadata.version("mcp")` | PASS：`2.3.0` |
| 手工 | `configure --apply` 后查看 `config.toml` 的 `[mcp_servers.*]` 标题 | PASS：仍有 `node_repl`，新增 `cursor-controller` |
| 手工 | 控制器 `doctor` | PASS 命令退出 0；结果 `available: false`，`agent_missing` |

## 未执行

- 项：在 Codex 新会话里调用 `cursor_doctor` / 其它控制器工具
- 原因：MCP 要等 Codex 重载配置；本机 PATH 和常见安装位置都没有 `agent` / `cursor-agent`
- 项：安装或配置 AOCI
- 原因：用户这次要的是新 kit，以及 Codex 上的新技能和 MCP；AOCI 是另一组件，这台机器没有 `~/.local/share/ai-agent-config/aoci`

## 结论

- 需求是否覆盖：仓库已与远端对齐；Kit v1.7.1 已进 Cursor、Claude 和这台机器的两处 Codex 技能目录；控制器技能与 MCP 已写入 Codex 用户配置。
- 旧功能是否破坏：Codex 原有 `node_repl` 配置仍在；旧 Kit 有备份。
- 剩余风险：没有 Cursor Agent CLI 时，已注册的 MCP 不能真正派任务。当前 Cursor 会话也不能使用这个只配给 Codex 的服务。
- 建议人工再验：装好官方 Cursor Agent CLI 并登录后，新开 Codex 会话再跑一次 `cursor_doctor`。
