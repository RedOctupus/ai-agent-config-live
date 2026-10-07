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
| R7 | 本仓自身可用 kit 交接（本仓路径是 `memory/kit/`） | 存在 MEMORY 及源文件，`python scaffold/scripts/check-memory-size.py` 退出 0 | 已对照 | 见 annex/VERIFY-20260921-init-memory-kit.md |
| R8 | 脚手架、记忆、本地物料分开放；密钥/取证/本机临时夹进 gitignore | 根目录仅入口文档；三层目录存在；`.gitignore` 含 `.env`、`_raw`、`materials/_local` | 已对照 | 见 annex/VERIFY-20260921-classify-repo-layout.md |
| R9 | 涉及 Agent / 能力模块 / 角色视图 / 多 Agent / 记忆读写 / 跨域流程时，先经过业务上下文优先设计门闸 | 能识别 L0–L3；L2/L3 明确业务域、生命周期、角色任务、上下文、Agent 边界、原子能力、视图和跨域回流 | 已对照 | 见 annex/VERIFY-20260927-business-context-agent-design.md |
| R10 | Kit 项目有可选 `BUSINESS-CONTEXT.md` 槽位，详情回 REQUIREMENTS / FLOW / FRAMEWORK | 两份 kit 模板含同名文件；不创建平行 `agent-design/` 记忆树 | 已对照 | 见 annex/VERIFY-20260927-business-context-agent-design.md |
| R11 | 无 Kit 的 Agent 项目可用独立 Skill 的兼容模式初始化最小业务上下文槽位 | Skill 说明 `docs/agent-context/`，且不覆盖已有项目文档 | 已对照 | 见 annex/VERIFY-20260927-business-context-agent-design.md |
| R12 | Agent-to-Agent 协作先有输入/输出契约；Agent 与能力模块按多对多建模 | `BUSINESS-CONTEXT.md` 含协作契约表、模块复用说明和前门闸；具体编排框架不在 Kit 中拍板 | 已对照 | 见 annex/VERIFY-20260927-business-context-agent-design-v1.5.md |
| R13 | Kit 的单人/多人骨架与 AOCI 启用彼此独立；单人 clone 不强制另建工作区，未启用时明确 Kit-only | 模板/CLI fixture 各验证默认未启用、单人 ready、无 MCP 安装 | 已对照 | 见 annex/VERIFY-20261006-aoci-workspace-kit-v1.7.md |
| R14 | 多人按 clone/worktree 隔离，拉取代码的新 Agent 在写源码前得到集成分支准入提醒；不静默创建，不以人员或模块充当工作区 | 常驻入口提醒；显式 status/create 实测，集成分支阻断、功能分支放行、冲突不自动处理 | 已对照 | 同上 |
| R15 | 个人 AOCI 地图只作提案，集成负责人先合源码，再在合并后的源码上更新全局地图；Kit/AOCI 可分别升级 | 两分支与集成工作区真实 Maintain/Verify/Check/Guide；Skill 不内嵌版本状态机；跨版本升级仍需另验 | 部分对照 | 同上 |
| R16 | Codex、Claude Code、Cursor 三宿主各在独立工作区做真实 MCP/认知验收，不用配置或模拟器冒充 | 三宿主真实会话最终 Host delivery confirmed、Attestation 10/10；Cursor 需隔离试验的宽授权模式，不代表默认自动调用 | 已对照 | 同上 |
| R17 | 已启用 AOCI 的项目可从 Kit README 按版本无关清单发起升级，不自动升级 Kit/AOCI、覆盖配置或重建索引 | 双权威 README 有目标版本确认、旧版冻结、新包校验、宿主实测、工作区回归和失败回滚门闸；TDD 定向及全量回归 | 已对照（文档入口；未执行跨版本升级） | 见 annex/VERIFY-20261006-aoci-upgrade-checklist.md |
| R18 | 拉取本仓即可取得 Kit 和 AOCI 发布包，用显式命令独立更新/配置；本轮更新三宿主 Kit，MCP 绑定当前配置仓并同步远端 | 11 项安装器 TDD、真实包离线冷安装、三宿主接入、备份与旧版本保留；不初始化现有业务项目地图 | 已对照（部署及远端拉取安装） | 见 annex/VERIFY-20261006-memory-tools-deploy.md |
| R19 | 按用户授权在 Cursor User Rules 仓内文档融合 STE 核心原则，保留既有操作协议，并明确中英文、精度与输出格式边界 | 规则 3 / 4、英文技术文本、冲突裁决和语言条款可逐项对照；原提交 / PR / 网页验收 / 规则 1 / 2 / 5 及既有 Superpowers 条款保留；仓内修订不冒充账号已同步 | 已对照（文档验收；未验证账号会话） | 见 annex/VERIFY-20261007-cursor-user-rules-ste.md |
| R20 | 技能条款保留交付前的 Kit / AOCI 调用入口，收尾详则由项目 MEMORY、Kit 与当前 AOCI Guide 管理 | Kit 已使用、AOCI 已启用且修改受管源码的条件明确；记录落点、执行顺序与未完成说明不在 User Rules 重复展开 | 已对照（文档验收；未验证账号会话） | 见 annex/VERIFY-20261007-cursor-user-rules-compact.md；原详则新增见上一轮 VERIFY |
| R21 | 整体压缩 User Rules，只去重与缩句，不放宽权限、精度或个人表达偏好 | 条款逐项对照；Git 授权和 amend 细则保留；表述 / 规则 1 / 规则 2 与其他 Skill 触发保持原文；同一编码比较压缩前后体量 | 已对照（文档验收；未验证模型执行效果） | 见 annex/VERIFY-20261007-cursor-user-rules-compact.md |
| R22 | 提供可复制粘贴的语义标记 TXT，将优先级、触发条件、权限例外、适用范围与输出时机明确分块 | TXT 为 UTF-8，无维护元信息；13 个语义块全部保留 MD 正文，仅增加标签和调整顺序；README 明确 MD / TXT 维护关系 | 已对照（格式与正文一致性；未测模型注意力效果） | 见 annex/VERIFY-20261007-cursor-user-rules-txt.md |

状态：`未做` → `开发中` → `已对照`。
