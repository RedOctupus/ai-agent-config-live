# 项目记忆包（project-memory-kit）

给**人和 Agent**用的可复用 init 包：新项目只落下少量活文档，不把整套行事哲学拷进去。

## 新项目怎么 init

1. 本机已同步到 `%USERPROFILE%\.cursor\skills\project-memory-kit\` 时，任意仓库说 `init 新项目` 即可（新开的 Cursor 窗口才一定加载得到）。
2. 否则：从权威源 [github.com/RedOctupus/ai-agent-config-live](https://github.com/RedOctupus/ai-agent-config-live) 的 `materials/agent-skills/<你的 Agent>/project-memory-kit/` 取，或对话里 `@SKILL.md`。
3. Agent 把 `templates/` 与体量门闸脚本拷到目标项目：

```text
docs/memory/MEMORY.md       # 各阶段一句话快照、约束、入口
docs/memory/ENVIRONMENT.md  # 服务对象大环境
docs/memory/REQUIREMENTS.md # 需求条目
docs/memory/FRAMEWORK.md    # 项目框架
docs/memory/FLOW.md         # 实现流程
docs/memory/BUSINESS-CONTEXT.md # Agent / 复杂业务上下文索引（L2/L3 可选）
docs/memory/TODO.md
docs/memory/ITERATION.md
docs/memory/HANDOVER.md     # 跨阶段必知事实（可增删改）
docs/memory/REFERENCES.md   # 外部对标 / 外部系统 / 来源的地址簿（可增删改）
docs/memory/annex/_TEMPLATE.md  # 选 VERIFY / NOTE / CHECKLIST / INDEX
docs/memory/annex/_INDEX.md     # 当日索引模板（真下发 INDEX-YYYYMMDD.md）
scripts/check-memory-size.py # 体量门闸（模板按项目内相对路径调用，故须随 init 落地）
scripts/kit-workspace.py # 多人源码写入前检查；只在显式 create 时新建 Git worktree
.gitignore（追加）           # 取证忽略片段：annex/_raw/ 不入库（templates/gitignore-memory.txt）
AGENTS.md
.cursor/rules/project-memory.mdc
```

默认**只** init 记忆目录 + 上述脚本。要 `.gitignore` / `.env.example` / `README.md` 骨架时，需另外点名「工程脚手架」。

## 希望任意仓库随口都能 init

把本目录同步到 Cursor **个人技能**（不要放进 `skills-cursor/`）：

```text
%USERPROFILE%\.cursor\skills\project-memory-kit\
```

Windows 示例：`C:\Users\Windows\.cursor\skills\project-memory-kit\`

**权威源在远端仓库，不在本机：**

```text
https://github.com/RedOctupus/ai-agent-config-live
  └── materials/agent-skills/claude/project-memory-kit/    ← Claude Code 副本
  └── materials/agent-skills/cursor/project-memory-kit/    ← Cursor 副本

装到本机（由上面拷贝，不是源）：
  → %USERPROFILE%\.agents\skills\project-memory-kit\     ← Codex
  → %USERPROFILE%\.claude\skills\project-memory-kit\
  → %USERPROFILE%\.cursor\skills\project-memory-kit\
```

> 路径含 `materials/` 前缀：本仓库做过目录三分（`scaffold/` · `memory/` · `materials/`），kit 落在 `materials/` 下。按 `agent-skills/...` 找会落空。

**版本：** 本 kit 当前 `v1.7.1`，见 `SKILL.md` 顶部 `kit-version`。项目侧在自己的 `MEMORY.md` §5 记下「按哪个版本建立」，用来判断是否该跟版（`references/migration.md` 二、骨架升级）。

改任一副本 → push 到该仓库 → 另一份同步 → `diff -r` 校验逐字一致，否则分叉。

同步范围：`SKILL.md`、`README.md`、`templates/`、`references/`、`scripts/`；**排除 `_sandbox/`**。

仍可用：把本仓库加进工作区，或对话里 `@SKILL.md`。已有 `docs/memory/` 但不合骨架 → 走 `references/migration.md` 收敛。

体量自检：`python scripts/check-memory-size.py [docs/memory/MEMORY.md]`，超阈值（全文 >400 行 / §0 **实义** >15 行或 >900 字符 / 单行 >300 字符）exit 1，裁剪 SOP 见 `templates/MEMORY.md` §5。
§0 只数**实义行**：空行、标题、`>` 说明块不计（它们不产生阅读负担，却会吃掉行预算）。脚本另会报告同目录 `HANDOVER.md` 行数，超 200 行给提醒，**不影响退出码**。

## 几份文档各写什么

| 文件 | 写 |
| --- | --- |
| `MEMORY.md` | **快照**：每阶段一句话 + 约束/入口。细节不写这里 |
| `ENVIRONMENT.md` | **服务对象大环境**（as-is）：服务谁、对方现在怎么办事 |
| `REQUIREMENTS.md` | **拆解条目**：可感知行为 + 验收句 + 状态 |
| `FRAMEWORK.md` | **项目框架**：技术选型（须用户逐项确认）、能力模块、分层 |
| `FLOW.md` | **实现流程**：端到端步骤、分支、每步 I/O |
| `ITERATION.md` | 变更记录（**只追加**） |
| `HANDOVER.md` | **跨阶段必知事实**：环境 / 路径 / 账号位置 / 工具版本 / 研究结论 / 坑 / 已排除的路。**可增删改**，不是追加 |
| `REFERENCES.md` | **外部参考地址簿**：对标产品文档 / 外部服务端点与本机路径 / 参考仓库 @ commit / 工具来源。**只放指针**，研究正文进 `annex/` 的 NOTE；**可增删改** |
| `annex/VERIFY-…` | **交付战报**：一任务一份，改了什么、跑过什么、结论 |
| `annex/INDEX-…` | **当日索引**：一天做成多件事时串成一份，只放指针。**不是工作日志，禁贴正文**；一天只有一件事就不建 |

项目做完一版：勾 `REQUIREMENTS` 状态；改对应源文件；MEMORY 只改变了的那句快照；写 ITERATION 和 VERIFY。  
**只有服务对象真实办事方式变了**才改 ENVIRONMENT。不要把源文件正文堆进 MEMORY。

日常阅读规则（含 TODO、annex、待办、`references/`）在项目里的 `MEMORY.md` 第 5 节，**不在**这份 README 里。Skill 只负责 init 和按需打开 `references/`。

## 多人 / 多模块

多个维护者 / 多模块、或有跨模块共享层（DB / 认证 / 接口）时 → `references/team.md`：按模块拆目录、owner 认领、大记忆不可动、共享层变更协议、merge 策略、kit 分发。

### 从本仓安装 / 更新三宿主

拉取本仓后，在仓根运行 `python scaffold/scripts/install-memory-tools.py install --apply`，更新 Codex / Claude Code / Cursor 的 Kit 与本机 AOCI；安装器保留旧技能与旧二进制。发布包与校验值都在仓内，init 不需要再次从 AOCI GitHub 下载。目标项目的 MCP 另用 `configure --repo <绝对 Git 根> --apply` 注册；Kit 更新用 `install --component kit --apply`，AOCI 更换版本先走下方升级清单。

完整命令、三宿主安装位置和回滚见源仓 `materials/tools/aoci/README.md`；本机源仓位置记录在 `~/.local/share/ai-agent-config/memory-tools.json`。本包适用于 Windows AMD64；每台机器、每个工作区都要按自己的绝对路径注册。

## AOCI 可选外挂与工作区

Kit 是 Skill，AOCI 是另装的项目级 stdio MCP，**AOCI 默认不启用**；Kit init 的单人/多人骨架与 AOCI 启用为两个独立选择。单人 clone 本身就是工作区，不强制创建 worktree。多人由用户在根 `ROOT-MEMORY.md` 确认集成分支；新人写源码前运行 `python scripts/kit-workspace.py status --repo . --mode team --integration-branch <已确认分支>`。集成分支须显式切到功能分支 clone/worktree，不静默创建，也不把人员或模块当工作区。

每个启用 AOCI 的工作区各配本机绝对 `--repo` 与宿主 MCP；参考[本试验所用 rc18 的官方宿主接入说明](https://github.com/aoci-spec/aoci-code/blob/v0.1.0-rc18/docs/agent-integrations.md)，正式部署须核对所选版本，不自动覆盖已有配置。个人地图只作提案；集成时**源码先于全局图**，合并后由集成 Agent 对真实源码重新维护 AOCI，Verify/Check/Guide 对齐后才交付。Kit 与 AOCI 可分别更新，不自动升级对方。未启用 AOCI 的项目仍按 Kit 槽位和源码/测试工作，不背地图维护债。

## AOCI 升级清单（仅已启用项目）

这是**升级入口与验收门闸，不是自动升级脚本**。先让用户确认目标版本、受影响的工作区/机器和宿主；Kit 版本不必跟着升级。具体兼容和迁移步骤以**目标版本**的发布说明及官方[升级](https://github.com/aoci-spec/aoci-code/blob/main/docs/upgrading.md)／[安装校验](https://github.com/aoci-spec/aoci-code/blob/main/docs/install.md)／[回滚](https://github.com/aoci-spec/aoci-code/blob/main/docs/rollback.md)文档为准（执行前核对对应 tag，不照搬旧试验版本）。

| 门闸 | 动作与通过条件 |
| --- | --- |
| 1. 升级前冻结 | 记录旧二进制绝对路径、版本、SHA-256，以及每个宿主配置中的命令和 `--repo`；保留旧二进制与配置备份。待恢复的 Guide、未完成事务或 Scope 审批须先完成/废弃，不跨版本带入。记录各工作区升级前对齐状态。 |
| 2. 核验新包 | 按目标版本官方说明校验发布包和身份，阅读兼容/许可变化；先与旧版并存，在一次性工作区核对 `--version`、能力清单及 `doctor`。失败即停，不自动覆盖正式二进制或宿主配置。 |
| 3. 切换宿主 | 经确认后替换稳定路径或逐机更新配置，只刷新仍运行旧进程的 MCP 连接。以 MCP 返回的**宿主实际运行版本**、仓库根与实际命令中的 `--repo` 为准；磁盘上的新文件或配置存在不算通过。 |
| 4. 工作区回归 | 在集成工作区和受影响的功能工作区，按目标版本当前 Guide 执行 Verify、Check、Guide；各实际宿主完成工具发现及当前规则/Overview/Attestation/目标 Entry 的真实调用。索引有漂移时按当前 AOCI 治理流程处理，**不重建索引**、不文本合并个人地图、不因换二进制强制更新 Baseline。 |
| 5. 放行或回滚 | 全部通过才记录版本、二进制 SHA、宿主身份、工作区验收和 Kit VERIFY/ITERATION/HANDOVER。失败则按官方回滚说明恢复旧二进制/配置并复验；若目标版本做了不可逆持久化迁移，先停下，不手改 `.aoci` 或强行回退。 |

Kit 只维护这套入口与停点，不复制 AOCI 的版本状态机；仅当新版本破坏 Kit 所依赖的 MCP/工作区能力契约，才另开 Kit 改动与 TDD。升级后 AOCI 不可用时标为“待维护”，不可静默改成“未启用”。


## Agent / 复杂业务设计接入

当任务涉及 Agent、能力模块、角色视图、多 Agent 协作、记忆读写或跨业务域流程时，先加载 `business-context-first-agent-design`。启用 Kit 的项目使用 `docs/memory/BUSINESS-CONTEXT.md` 作为业务上下文索引；它不替代 `REQUIREMENTS.md`、`FLOW.md`、`FRAMEWORK.md`。没有 Kit 的项目使用该 Skill 的 `docs/agent-context/` 兼容模式。
