# 项目交接文档（必知事实）

> 接手先看这里。事实仅供参考，用前核实；与现场冲突以现场为准。
> 2026-09-21 从 README、tools/catalog.md、memory 导出、git、本机 hostname 搜集；catalog 停在 2026-05-24。

**最后核实：** `2026-10-07` · HEAD `f4e3a7f`（家里台式机已快进 `origin/main`。Kit v1.7.1 已装到 Cursor、Claude、`~/.agents/skills`，并镜像到 `~/.codex/skills`。Codex 已注册 `cursor-cli-controller` 与 `cursor-controller` MCP。`doctor` 报本机没有 Cursor Agent CLI。本机未装 AOCI）

> 短哈希**只写这一处**。`MEMORY.md` §0「工作分支」只留分支名。

------

## 1. 运行环境

| 事实 | 值 / 结论 | 证据或出处 | 核实日期 |
| --- | --- | --- | --- |
| 本次所在机 | `SC-202601081030`（家里台式机） | 本轮 `COMPUTERNAME` | 2026-10-07 |
| 另一台 | 学校笔记本 `DESKTOP-DKO2LI9`；2026-10-06 的 Kit/AOCI 部署和 `C:\Users\Windows\...` 路径属于那台 | `materials/agent-skills/README.md`；此前交接 | 2026-10-07 |
| OS（档案） | Windows 10 workstation | `README.md` · `memory/hermes/machine.md` | 2026-05-24 |
| 本仓远程 | `https://github.com/RedOctupus/ai-agent-config-live` 私仓 | `git remote -v` · README | 2026-09-21 |
| 默认分支 | `main` | `git rev-parse` | 2026-09-21 |
| 本仓无常驻服务 | 备份仓，不跑 HTTP/DB | 目录结构 / README | 2026-09-21 |
| 业务上下文优先 Skill | 三份通用副本：`materials/agent-skills/{portable,claude,cursor}/business-context-first-agent-design/`；Kit 两份权威副本现为 v1.7.1，本机 Codex/Claude/Cursor 已按用户授权更新；`templates/BUSINESS-CONTEXT.md` 保留协作契约 | Kit 双副本字节一致、quick_validate PASS；此前 DeepSeek 六场景见旧 VERIFY | 2026-10-06 |

## 2. 关键路径

| 事实 | 值 / 结论 | 证据或出处 | 核实日期 |
| --- | --- | --- | --- |
| 仓库工作副本（本机） | `D:\11-AI Agent\agnet_config\ai-agent-config-live` | 本轮工作目录 | 2026-10-07 |
| 仓库工作副本（笔记本） | `D:\杂货铺\新建文件夹\ai-agent-config-live` | 2026-10-06 交接 | 2026-10-06 |
| Hermes 源码/安装 | `D:\09-其他\hermes-agent\` | `memory/hermes/machine.md` | 2026-05-24 |
| Hermes 本机配置 | `~/.hermes/`（config.yaml、skills、memories、state.db） | `memory/hermes/machine.md` | 2026-05-24 |
| Cursor 个人技能（本机） | `~/.cursor/skills/` | `materials/agent-skills/README.md` | 2026-09-21 |
| Claude 个人技能（本机） | `~/.claude/skills/`；家里台式机 Kit 已是 v1.7.1 | [VERIFY-20261007-desktop](annex/VERIFY-20261007-desktop-kit-controller-install.md) | 2026-10-07 |
| Codex 技能（本机） | 官方安装器写入 `~/.agents/skills/project-memory-kit`（v1.7.1）。这台 Codex 还从 `~/.codex/skills` 加载，该处 Kit 已从 v1.6.0 镜像为 v1.7.1，旧树在 backups。`cursor-cli-controller` 装在 `~/.codex/skills` | 同上 | 2026-10-07 |
| Cursor 个人技能（仓内） | `materials/agent-skills/cursor/` | 同上 | 2026-09-21 |
| Claude 技能（仓内） | `materials/agent-skills/claude/` | 同上 | 2026-09-21 |
| Hermes 技能（仓内） | `materials/skills/` | README Structure | 2026-09-21 |
| Hermes 配置（仓内） | `materials/hermes/` | README | 2026-09-21 |
| Hermes 记忆导出（仓内） | `memory/hermes/` | README；**不是** `memory/kit/` | 2026-09-21 |
| 本仓 kit 记忆 | `memory/kit/` | 本仓特例；其它项目 kit 默认仍是 `docs/memory/` | 2026-09-21 |
| Cursor 用户全局规则资产 | `materials/cursor-user-rules/`：`RULES.md` 是维护源，`RULES.txt` 是可复制的语义标记版。已融合 STE / Kit/AOCI 入口并压缩重复详则；TXT 保留 13 章正文；未写回账号，本仓不注入 | `annex/VERIFY-20261007-cursor-user-rules-txt.md`；各轮记录见当日 INDEX | 2026-10-07 |
| Superpowers 备份 | `materials/agent-skills/cursor/plugins/superpowers/` | agent-skills README | 2026-09-21 |
| AOCI 隔离沙盒 | `experiments/aoci-memory-kit/sandbox/ssss-agent/`。原 SSSS 不在这个地址，不要去原项目测 | 沙盒 `.codex/config.toml` 指向 `experiments/aoci-memory-kit/artifacts/bin/aoci.exe` | 2026-10-06 |
| AOCI 工作区试验 | `experiments/aoci-memory-kit/artifacts/workspace-fixtures/`（Git 忽略）；`integration` 与 `task-{codex,claude,cursor,merge-a,merge-b}` 各是独立绝对根。全局图只在集成源码之后重签；原 SSSS 330 文件未变 | `experiments/aoci-memory-kit/VERIFY-20261006-workspace-hosts.md` | 2026-10-06 |
| 本机 Codex CLI | `C:\Users\Windows\AppData\Local\OpenAI\Codex\bin\5ea220ae823df3d7\codex.exe`，`codex-cli 0.160.1`；当前会话 PATH 可用 | `codex.exe --version` | 2026-10-06 |
| 本机 Cursor Agent CLI | `C:\Users\Windows\AppData\Local\cursor-agent\cursor-agent.cmd`，`2026.10.01-e373342`；官方 Windows 安装与登录获本轮用户授权；隔离 worktree 用授权模式完成真实 AOCI MCP 会话 | `cursor-agent --version` / `status` 与本轮 VERIFY | 2026-10-06 |
| 脚手架脚本 | `scaffold/scripts/` | restore / sync / auto-sync / check-memory-size | 2026-09-21 |
| 体量门闸 | `python scaffold/scripts/check-memory-size.py`（默认 `memory/kit/MEMORY.md`） | 本仓脚本 | 2026-09-21 |
| Kit/AOCI 仓内安装来源 | `materials/tools/aoci/` 与 `scaffold/scripts/install-memory-tools.py`。学校笔记本已有 EXE `~/.local/share/ai-agent-config/aoci/0.1.0-rc18/`，并给那份工作区配了 MCP，索引未初始化。家里台式机本次没有安装 AOCI | `annex/VERIFY-20261006-memory-tools-deploy.md` · [VERIFY-20261007-desktop](annex/VERIFY-20261007-desktop-kit-controller-install.md) | 2026-10-07 |
| 本机临时物料 | `materials/_local/`（gitignore） | `.gitignore` | 2026-09-21 |
| Cursor Controller 来源与安装 | 原创建 0.1.0 在 `materials/agent-skills/codex/cursor-cli-controller/`。家里台式机已把技能和 `cursor-controller` MCP 写入 Codex 用户配置；`doctor` 返回 `agent_missing`，PATH 里没有 Cursor Agent CLI。审计目录与 Kit 独立 | `annex/VERIFY-20261007-cursor-cli-controller.md` · [VERIFY-20261007-desktop](annex/VERIFY-20261007-desktop-kit-controller-install.md) | 2026-10-07 |

## 3. 账号与凭据位置

| 事实 | 值 / 结论 | 证据或出处 | 核实日期 |
| --- | --- | --- | --- |
| GitHub | 账号 RedOctupus；gh 在 `C:\Program Files\GitHub CLI\gh.exe` | `memory/hermes/environment.md` | 2026-05-24 |
| 机主档案 | `memory/hermes/user-profile.md`（含邮箱；勿把密钥抄进本文件） | 该文件 | 2026-05-24 |
| Hermes / LLM key | **只在本机** `~/.hermes/.env`；仓内 `materials/hermes/.env.template` | README Quick Recovery | 2026-09-21 |
| OpenAI Pro / Codex | 档案写已订阅；登录方式见 `materials/tools/catalog.md` | catalog | 2026-05-24 |

## 4. 工具链版本

| 事实 | 值 / 结论 | 证据或出处 | 核实日期 |
| --- | --- | --- | --- |
| 档案快照（可能过期） | Hermes 0.14.0；Codex 0.133.0；gh 2.92.0；git 2.53.0；Node 24.14.0；Python 3.11.14/3.13.9 | `README.md` · `materials/tools/catalog.md` | 2026-05-24 |
| 本次会话本机抽查 | git `2.55.0.windows.3`；Node `v22.23.1`（Winget Node 22 路径） | 同机其它任务 `git --version` / `node -v` | 2026-09-21 |
| Codex CLI（现场） | `0.160.1`。档案里的 Codex `0.133.0` 已过期 | `codex.exe --version` | 2026-10-06 |
| GPU 档案 | RTX 5070 Ti 16GB；CUDA driver 13.2 / toolkit 13.1 | `memory/hermes/machine.md` | 2026-05-24 |
| catalog 维护说明 | Git Bash (MSYS) 不用 PowerShell；与 Cursor Agent 常用 PowerShell **可能不一致** | `materials/tools/catalog.md` | 2026-05-24 |
| project-memory-kit 版本 | **仓内权威副本 `v1.7.1`**。家里台式机的 Cursor、Claude、`~/.agents/skills`、`~/.codex/skills` 四份文件已对齐该版本。本机没有 AOCI 二进制 | 安装器 `filecmp` · [VERIFY-20261007-desktop](annex/VERIFY-20261007-desktop-kit-controller-install.md) | 2026-10-07 |

## 5. 研究结论（已确认）

| 事实 | 值 / 结论 | 证据或出处（**必填**） | 核实日期 |
| --- | --- | --- | --- |
| kit 权威源在本仓 | Cursor/Claude 两份 `project-memory-kit` 应逐字一致 | kit `SKILL.md`「改 kit 本身」 | 2026-09-21 |
| 本仓 kit 路径是特例 | 本仓用 `memory/kit/`；kit 模板副本仍写 `docs/memory/`（给其它项目用） | 用户要求三分目录；未改 kit 模板 | 2026-09-21 |
| 根目录无 AGENTS.md（init 前） | 本次由模板生成 | `Test-Path AGENTS.md` 曾为 False | 2026-09-21 |
| kit 提供「当日索引」 | 一天做多件事时用 `annex/INDEX-YYYYMMDD.md` 串起当日指针（**不是工作日志，禁贴正文**）；一天只有一件事则不建。**init 拷的是模板 `_INDEX.md`**（v1.1.1 改名，避免与带日期文件撞名；该改名后版本号纠正为 v1.2.0） | kit `templates/annex/_INDEX.md` · `annex/VERIFY-20260921-kit-v1.2.1.md` | 2026-09-21 |
| 短哈希只在一处 | MEMORY §0「工作分支」**只留分支名**；短哈希只写本文件顶部「最后核实」（改本文件才刷）。v1.3.0 前两处都记哈希，两种时钟会被误当成漏刷 | kit `templates/MEMORY.md` §0 · `templates/HANDOVER.md` · `annex/VERIFY-20260921-kit-v1.3.0.md` | 2026-09-21 |
| Kit×AOCI 实验结论 | 项目受信任、宿主批准后，独立 worktree 的 Codex/Claude/Cursor 真实会话可完成 Host delivery 与严格 Attestation；两个人图经源码先行集成后可重新签发全局图。Kit v1.7.0 **只提供可选接口**，不对既有项目自动启用 | `annex/VERIFY-20261006-aoci-workspace-kit-v1.7.md` | 2026-10-06 |

## 6. 已知的坑 / 反直觉行为

| 事实 | 值 / 结论 | 证据或出处（**必填**） | 核实日期 |
| --- | --- | --- | --- |
| 两套 memory 仍分开 | `memory/hermes/` = Hermes 导出；`memory/kit/` = 本仓 kit | README Structure | 2026-09-21 |
| 同步默认单向 | 日常仍不静默拷回本机；本轮三宿主 Kit/AOCI 安装由用户明确授权，后续更新走仓内显式命令 | `materials/agent-skills/README.md` 第 2 条；部署 VERIFY | 2026-10-06 |
| 版本清单易过期 | Last sync 2026-05-24 与 2026-09-21 现场 git/node 已对不上 | README vs 本机命令 | 2026-09-21 |
| 恢复脚本是 sh | 笔记本上若只用 PowerShell，须用 Git Bash 跑 `./scaffold/scripts/*.sh` | `scaffold/scripts/*.sh` · catalog「Always use POSIX」 | 2026-09-21 |
| 脚本相对根目录上移一层 | 脚本在 `scaffold/scripts/`，`REPO_ROOT` 是 `dirname $0/../..` | restore.sh 注释 | 2026-09-21 |
| Codex 不加载未受信任项目的 MCP | 项目级 `.codex/config.toml` 只有 `trust_level = "trusted"` 后才进新会话。本轮另按用户授权信任了当前配置仓，临时 worktree trust 未扩散 | `~/.codex/config.toml` 的 `projects` 段 | 2026-10-06 |
| `codex exec` 默认不审批 | 能看见 `aoci_rules`，调用返回 approval policy is never。`--approve-for-me` 不能和 `--sandbox read-only` 同用；批准路径具备工作区写入能力 | 同日两次 `codex exec` 日志 | 2026-10-06 |
| AOCI receipt 不能猜版本 | 两宿主首次认知测试均模型误填 delivery confirmation 版本，虽 Attestation 10/10，Host delivery 仍 incomplete；新会话用本次 Overview 返回的 `delivery_receipt_version` 后才完整通过 | `experiments/aoci-memory-kit/VERIFY-20261006-workspace-hosts.md` | 2026-10-06 |
| Codex 临时 trust 清理 | worktree 试验临时项目 trust 标记已移除；用户配置 SHA 与试前记录不一致，未整体覆盖配置以免抹掉并发编辑 | 忽略的 `artifacts/raw/codex-temporary-trust.json` 与复核 | 2026-10-06 |
| Cursor 宿主授权差异 | `mcp list` ready 不等于模型会话可调用；CLI `ask` 模式未暴露项目 MCP，普通非交互会话调用被拒。隔离试验仅在 `-p --trust --approve-mcps --force` 下真实通过；正式项目须另找最小审批路径 | `experiments/aoci-memory-kit/VERIFY-20261006-workspace-hosts.md` | 2026-10-06 |
| AOCI 升级边界 | rc18 现已从仓内包首次部署三宿主；没有跨 AOCI 版本或第二台机器实测。后续先确认目标版本并完成升级清单，再显式安装/逐工作区切换，Kit 不自动跟版 | 双权威 README；`annex/VERIFY-20261006-memory-tools-deploy.md` | 2026-10-06 |

## 7. 已排除的路（别重试）

| 事实 | 值 / 结论 | 证据或出处（**必填**） | 核实日期 |
| --- | --- | --- | --- |
| 备份 Cursor 内置技能 | 明确不含 `~/.cursor/skills-cursor` | `materials/agent-skills/README.md` | 2026-09-21 |
| clone 完自动注册全部技能 | 「不自动拉本机、不自动注册」 | 同上第 2 条 | 2026-09-21 |
| 改 kit 模板里的**默认路径**来迁就本仓 | 其它项目仍用 `docs/memory/` | 用户约束：不改 kit 副本的默认路径。**改副本内容本身是允许的**——走 kit `SKILL.md`「改 kit 本身（同步）」，两份保持一致即可（2026-09-21 用户即指派迭代 kit，见 `ITERATION.md`） | 2026-09-21 |

------

## 不写什么（落笔前看一眼）

| 这类内容 | 写到哪 |
| --- | --- |
| 密钥 / token / 密码本身 | **哪都不写**（只写位置，见第 3 节） |
| 函数实现、文件清单、步骤 | Plan / 代码 |
| 逐轮验证结果 | `memory/kit/annex/` |
| 「为什么变成现在这样」 | `ITERATION.md` |

