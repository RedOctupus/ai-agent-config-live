# VERIFY：家里台式机安装 Cursor Agent CLI

- 日期：2026-10-07
- 关联 TODO：无（用户要求按官网安装，并处理上次没推上去的提交）
- 风险等级：LOW

## 改了什么

- 上次本地提交 `eaca31e` 已推到 `origin/main`。
- 按 [Cursor CLI 文档](https://cursor.com/docs/cli/overview) 的 Windows 命令安装：`irm 'https://cursor.com/install?win32=true' | iex`。
- 安装脚本标明版本 `2026.10.01-e373342`，包来自 `https://downloads.cursor.com/lab/2026.10.01-e373342/`。
- 用户 PATH 增加了 `%LOCALAPPDATA%\cursor-agent`。安装前该目录不存在，脚本里的删除步骤没有删掉已有文件。

## 已执行

| 类型 | 命令或步骤 | 结果 |
| --- | --- | --- |
| 手工 | `git push origin main` | PASS：`f4e3a7f..eaca31e` |
| 手工 | 官网安装命令 | PASS：打印 “Happy coding!”，退出码 0 |
| 手工 | `agent --version` 与 `cursor-agent --version` | PASS：两者都是 `2026.10.01-e373342` |
| 手工 | 控制器 `doctor` | PASS：`available: true`；路径 `...\cursor-agent\agent.cmd`；所需旗标都在；认证 `unauthenticated` |

## 未执行

- 项：`agent login`
- 原因：登录要用户在本机完成，这次没有代为打开登录流程

## 结论

- 需求是否覆盖：未推送的提交已在远端；CLI 已按官网脚本装上，控制器能找到它。
- 旧功能是否破坏：没有覆盖已有 `cursor-agent` 目录。
- 剩余风险：未登录时控制器不能派真实任务。已经开着的终端要重开，才会从用户 PATH 里看见 `agent`。
- 建议人工再验：在新终端执行 `agent login`，然后再跑一次 `doctor`。
