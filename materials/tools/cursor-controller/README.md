# Cursor CLI Controller 0.1.0

这套技能让 **Codex 协调、Cursor 执行、本地 MCP 记录独立审计**。Codex 根据任务选择原生 subagents、TDD、调试或直接执行，监控任务并独立验收。执行成功、测试通过、技术拍板、记忆回写分别记录；续接会创建新执行批次。

源码只有一份：[Codex 技能目录](../../agent-skills/codex/cursor-cli-controller/)。这里放介绍、前置、来源/版本和分发清单；不复制一套运行核心。

## 使用前置

| 前置 | 检查方法 | 缺失时 |
| --- | --- | --- |
| Windows 原生 Cursor Agent CLI | `agent --version`、controller `doctor`；编辑器 `cursor` 命令不能代替 Agent | 按官方 CLI 安装说明安装，不把 WSL 命令当成本机原生工具 |
| 当前 Cursor 登录 | `doctor` 只返回脱敏认证状态 | 用户完成 `agent login` 或已有环境认证；密钥不写进仓库/任务契约 |
| Python | 安装器需要 Python 3.11+；本次实际验证 3.13.9 | 使用已有支持版本；依赖只进技能私有 `.venv` |
| 官方 MCP SDK 2.3.0 | `requirements.txt` 固定版本，安装器仅在私有环境缺失/版本不符时安装 | 初装需要包源联网；仓库不捆绑 SDK wheel 或 `.venv` |
| Codex 的 `cursor-controller` MCP | 注册后用 `cursor_doctor` 确认真实工具可调用；CLI 同核心可作兼容入口 | 只添加本服务配置，保留其他服务；必要时在宿主重新加载 |
| Windows 后台执行设施 | PowerShell、Task Scheduler、同解释器旁的 `pythonw.exe`、当前用户交互会话 | 不确定启动保留租约并报诊断；不静默提权、安装系统服务或宣称任务存活 |
| 目标项目与写入责任 | 读取项目入口、既有改动，明确目标/可改路径/验收 | 不启动重复或路径重叠的写入者 |
| MEMORY kit | `cursor_capabilities` 返回项目记忆入口、schema 版本、AOCI 状态 | **没有 Kit 可正常用**；不自动初始化 Kit，不把不可读当作没有 |
| 已启用 AOCI | 在该工作区实际配置的宿主按当前服务/Guide维护 | 已启用但不可用保留“待维护”；仅注册、尚未初始化不算启用 |

Kit 是可选的项目记忆规范。MCP 始终独留一份机器审计；有 Kit 时 VERIFY/ITERATION 引用 task/run/回执，原始日志不塞进 MEMORY。

## 从本仓安装

在仓根执行，默认都是预览/检查，写入要加 `--apply`：

```powershell
python scaffold/scripts/install-cursor-controller.py verify
python scaffold/scripts/install-cursor-controller.py install
python scaffold/scripts/install-cursor-controller.py install --apply
python scaffold/scripts/install-cursor-controller.py configure
python scaffold/scripts/install-cursor-controller.py configure --apply
```

默认技能位置是 `$CODEX_HOME/skills/cursor-cli-controller`，未设 CODEX_HOME 时为 `~/.codex/skills/cursor-cli-controller`。MCP 只给 Codex 配置，Cursor 继续使用自己的工具。初次注册使用独立、稳定的 `~/.local/share/ai-agent-config/cursor-controller/audit`，也可显式 `--data-dir`。

安装器验证 manifest 的逐文件 SHA-256，保留目标 `.venv`。相同文件重复安装不改写；已装源码不同则停止，不静默覆盖。升级时先停止相关任务/重载 MCP、备份旧源码，再显式选择新安装位置；审计目录与技能源码分离。同名 MCP 配置不同也停止；已有服务可以继续使用，先读 `cursor_doctor.data.data_dir`，不要为了重注册丢掉旧审计。

配置仅追加本服务，并备份旧 TOML，原有服务器、字段和注释保留；本机绝对路径写到用户配置，**不进 Git**。不自动向 Cursor/Claude 注册调度工具，不安装或升级 Kit/AOCI。

## 使用

```text
使用 $cursor-cli-controller，让 Cursor 在指定项目完成这项任务；
你自行选择 subagents/TDD 等工作方式，监控进度，独立验收并保存责任战报。
```

首次调用：doctor → capabilities(目标工作区) → 明确任务契约 → submit → watch/status → 写回必要记忆 → final verify → 记录验收/署名。

协调端负责用户沟通、任务范围、项目级记忆整合和技术验收。Cursor 决定实际工具与实现步骤，并写获准的模块记忆/执行事实。每次战报记录执行者、作者、审阅者、拍板者、时间、依据和回执；未审阅/未拍板标 pending，不冒充用户确认。多人维护的回执保留每个维护者，而不把所有工作署名给战报作者。

详细契约见 [调用端与记忆责任](../../agent-skills/codex/cursor-cli-controller/references/calling-and-memory.md)；命令、回执、失败恢复见 [操作参考](../../agent-skills/codex/cursor-cli-controller/references/operations.md)。

## 来源与版本

| 资产 | 版本/定位 | 来源性质 |
| --- | --- | --- |
| Skill + 原创运行核心 | 0.1.0；以本仓 Git 提交与 `VERSION` 定位 | 按本轮用户批准的设计原创；非 Cursor 产品副本 |
| MCP SDK | 2.3.0 | 官方 Python SDK，MIT，安装到私有环境 |
| Cursor Agent CLI | 本次验证 2026.10.01-e373342 | 机主已有官方安装；不捆绑二进制 |
| Python | 本次验证 3.13.9 | 机主已有解释器；安装器要求 3.11+ |
| Kit 参考规范 | 已安装参考 1.7.1；项目 schema 单独检测 | 复用本仓 Kit，不修改两份权威副本 |

原始控制器未另行声明开源许可，按本私仓权限保留；SDK 的 MIT 不自动覆盖原创代码。版本、来源和源码完整性在 [manifest.json](manifest.json) 与技能 [SOURCE.md](../../agent-skills/codex/cursor-cli-controller/SOURCE.md)。

官方依据：[Cursor CLI](https://cursor.com/docs/cli/overview)、[输出格式](https://cursor.com/docs/cli/reference/output-format)、[Subagents](https://cursor.com/docs/subagents)、[MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)、[MCP 工具协议](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)、[Codex MCP](https://developers.openai.com/codex/mcp)。

## 验证与边界

分开记录真实 Cursor 验证、模拟进程/协议回归、技能行为评估与安装器测试。真实隔离任务验证了原生 Task/explore 分工、TDD RED→GREEN、独立复验、会话续接和责任报告；完整结果见本仓对应 VERIFY。

Windows 的后台持久性验证使用未修改的官方 MCP 客户端，覆盖运行中及刚提交即断开。后台 worker 采用当前用户、最低权限、一次性隐藏 Scheduler 启动，验证身份后删除自己的启动项，无周期触发或常驻系统服务。重启、退出用户会话、Scheduler 不可用或磁盘持续故障不承诺自动恢复；不确定写者不会被当作已停止。

POSIX 分支未在本次 Windows 会话实测。文件哈希与责任署名用于追踪，不能认证人类身份，也不宣称审计不可篡改。运行数据、账户信息、本机配置、虚拟环境、原始模型/命令日志不随源码提交。
