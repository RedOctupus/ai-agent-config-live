# Cursor CLI Controller 0.1.0 发布验收

日期：2026-10-07（Asia/Shanghai）。用户授权先头脑风暴，再实现 Codex→Cursor CLI 分配、监控、验收；批准 MCP 独立审计，并授权责任细则落新 Skill、整理指定仓库与同步远端。

## 责任署名

| 责任 | 实际主体 | 信息地位 |
| --- | --- | --- |
| 实现执行 | Codex 协调会话与运行时实现/修复子 Agent；真实执行验证由 Cursor CLI 会话完成 | 本轮实际工具与报告记录；非用户亲审 |
| 战报作者 | Codex 当前协调会话 | declared；依据实际日志/回执整理 |
| 源码审阅 | 独立 `release_rereview` Agent；原五项问题与混合维护者问题经修复后 GO | 独立源码/证据审阅，未冒充重新运行完整测试 |
| 技术拍板 | Codex 依据实测与独立审阅作技术验收 | delegated；用户授权实施与发布，未声明用户亲自审核代码 |
| 归档/安装器验证 | Codex 当前协调会话 | 独立逐文件一致性、安装器回归和隔离冷安装 |
| 用户决策依据 | “决策可以，mcp独留一份审计”“测试没问题后…整理到…ai-agent-config-live…和远端同步” | 实际用户授权；不等于虚构用户测试/审阅 |

## 交付位置与版本

- 单源码：`materials/agent-skills/codex/cursor-cli-controller/`，VERSION 0.1.0。
- 前置、介绍、来源：`materials/tools/cursor-controller/README.md` 与 manifest。
- 显式安装器：`scaffold/scripts/install-cursor-controller.py`；默认预览、不静默覆盖已装版本或同名 MCP。
- 官方 MCP SDK 2.3.0；实测 Python 3.13.9、Cursor Agent CLI 2026.10.01-e373342。
- 未修改 Kit 双权威副本；本仓记忆位于 `memory/kit/`，schema v1.5.0；AOCI 为 configured_not_initialized，未自动建图/调用维护。

## 验证结果

| 验证 | 结果与实际范围 |
| --- | --- |
| 控制器全量 | 61 项，59 执行通过，2 项因 Windows symlink 权限跳过；退出 0。包含真实本地进程、Job、Scheduler、官方 SDK stdio 断连、租约与回执版本验证 |
| 安装器 TDD | 先 7 项失败（实现缺失），后 9 项通过（新增入口路径/审计隔离2项先RED后GREEN）；覆盖来源哈希、越界路径、默认预览、不覆盖用户版本、私有环境保留、配置文本/其他服务保留、同名冲突 |
| 隔离冷安装 | 源码21文件从本仓装入临时独立目录，私有 SDK 安装、doctor 认证检查、临时 MCP TOML 配置通过；doctor显式使用临时audit；未改全局配置 |
| 真实 Cursor TDD | 先 4 个失败单测，再实现、4 项单测通过；Codex通过 MCP 独立执行单测及5用例行为 oracle。中文/空格/`&`工作区及 UTF-8 契约保持 |
| 原生 subagents | Ask 只读模式中两次真实 Task/explore 启动与完成事件，父 Agent 汇总；不是仅凭模型声明 |
| 真实续接 | 同一 Cursor 会话新增 run/revision2；旧验证被 stale_run 拒绝，新责任报告 pending后重新独立验收 |
| Kit 入口检测 | 无 Kit 可用；正常 docs/memory 与本仓 memory/kit 识别；v1.5 schema 不被顶部v1.7进度覆盖；已启用但不可用不降为disabled；配置未初始化单列 |
| 混合维护者 | 每个维护 action 单独 performed_by/证据/回执；合并覆盖所需路径；不把 Cursor 模块维护署名给 Codex 战报作者；旧单人收据兼容 |
| 独立审阅 | 发现并修复 launch后错误释放租约、Windows连接杀子进程、已拍板后验证变更、记忆哈希顺序、维护者错误署名；混合维护者复审 GO |

本地原始测试/模型/命令日志与机器配置保留在忽略的取证位置，不提交到 Git。仓库 manifest 保存源码 SHA-256；哈希不是身份认证或不可篡改承诺。

## 独立审计回执摘要

MCP 审计独立于 Kit。此文只引用实际标识和结论，不复制原始 JSON/模型文本：

- TDD task `01935ea6e5b543d9a290e6b987363ebf`，当前 run `e6287283088e4ffd8b98ac95241fb6c9`，Cursor session `5e84bd1b-281a-4c80-b399-00da114248de`；验证回执302、技术决策303、署名报告304；7项机器证据。
- Explore task `17a0ec20a21144bc956b481577969c77`，run `75b23b428dda4ba8812f44023746ea99`，session `6c9ba557-8f5c-4a1d-8530-a7f1d4b20cc7`；验证308、技术决策309、报告310；4项机器证据；两子 Agent ID可由同一任务原始事件追溯。
- 这些是开发隔离验证回执，不是本仓发布提交的密码学签名。技术决策者/作者为 Codex，执行主体为实际 Cursor 会话。

## 已知范围

Windows 主路径已验证；POSIX 未实测。Scheduler 需要当前用户交互会话及其可用服务；不承诺重启/用户退出/持续磁盘故障自动恢复，不确定写者保留租约。AOCI 回执在本次使用 fixture 检查署名/链接，未声称实际调用启用项目 AOCI。Skip 的两项 symlink边界不能写成实测通过。

## 远端同步

本地与 origin/main 发布前基线一致。本次只提交控制器、介绍/安装器及相关项目记忆；无关未跟踪框架文件保留。推送结果待本轮提交后核对，并写入 HANDOVER 与后续同步记录。
