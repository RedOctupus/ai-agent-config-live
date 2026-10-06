# Kit × AOCI：可选部署契约

> 本文是隔离试验的部署契约。Kit 权威副本仅更新 Skill/模板/工作区检查脚本；不会向现有项目自动安装 MCP、升级 AOCI 或覆盖宿主配置。

## 两个组件，不是两个 MCP

- **Kit 是 Skill，不是 MCP**：Coding Agent 通过已安装的 Kit Skill 初始化项目记忆；项目日常只读自己的 `MEMORY.md`，其入口/槽位负责提醒。
- **AOCI 是项目级 stdio MCP**：同一个 AOCI 二进制可服务多个工作区，但每个启用的 clone/worktree 要有自己的绝对 `--repo`、索引/基线和项目级宿主配置。宿主在需要时启动当前工作区的 MCP 进程，不需另建常驻网络服务。可用工具、Guide 和语义维护归 AOCI 当前版本，不由 Kit 实现第二套状态机。
- AOCI 发布包/许可/宿主接入需在实际目标项目逐项得到用户同意。本次试验同意只对沙盒有效。AOCI 默认离线确定性模式；额外 AI 端点、业务数据库和自动 hooks 均不是这个方案的部署前提。

## Kit init 的两个正交问题

| 问题 | 决定 | 默认/未答 |
| --- | --- | --- |
| **单人 / 多人？** | 单人用普通 `MEMORY.md`；多人用根 `ROOT-MEMORY.md`、`OWNERS.md` 与模块 MEMORY。 | 用户独自 clone 时按单人，不强制问或建 worktree；明确多人或不明时问。 |
| **AOCI 源码地图启用 / 不启用？** | 启用才开始 AOCI 安装与项目级 MCP；不启用明确写“未启用”。 | 不自动安装；状态“未启用／待确认”。 |

两问彼此独立。团队的**每个工作区先维护自己的地图**；根状态由架构负责人维护，模块 MEMORY 指向根状态。模块复用单人 MEMORY 模板时，init 必须把默认“未启用”替换为指向根 `ROOT-MEMORY.md` 的相对链接。新人拉取后，入口先读取根文件的**人类确认的集成分支**；团队源码写入前跑 `python scripts/kit-workspace.py status --repo . --mode team --integration-branch <分支>`。处在集成分支时须显式创建/切换独立功能工作区，不静默创建；功能分支 clone/worktree 可直接用。Git 本身无法证明该目录没有另一个 Agent 同时写入，还须约定独占写入。

## 启用路径

1. Kit 先选单人/多人骨架，生成/合并记忆，不覆盖现有用户文件。选择不启用 AOCI 时到此为止，目标 MEMORY（多人为根负责槽位）保留“未启用”；不运行 `aoci init`，不注册 MCP。
2. 明确启用后，选定受支持 Coding Agent，核验 AOCI 版本/许可/官方安装来源。对一个 Git 仓运行 `aoci --repo <绝对仓路径> init --agent <宿主>`（只对用户批准的目标仓）。**Codex** 写项目 `.codex/config.toml`；**Claude Code** 写项目 `.mcp.json`；**Cursor** 在当前 rc18 仅给参考 `.cursor/mcp.json`，需人工核实后配置，不称作自动安装。[官方宿主接入说明](https://github.com/aoci-spec/aoci-code/blob/v0.1.0-rc18/docs/agent-integrations.md)。
3. 宿主配置含二进制与**当前工作区**的绝对路径，不得提交；应确认 `.gitignore`、是否已有同名配置、项目是否受信任以及 MCP 工具是否在当前会话可见。改配置后若当前会话未加载，刷新该项目会话，不要求盲目重启全部宿主。每台机器、每个工作区各自配置本机路径，不复制他人配置或运行时事务。
4. 首次 `scan` 前决定 Managed Scope。之后按当前 AOCI Guide 进行模型撰写、校验和对齐；`doctor`、`verify`、`check` 与 Guide 验证完成后，Kit MEMORY 状态才从“未启用／待确认”改为“已启用”，留一个到根 `AGENTS.md` AOCI 区块的指针。Kit 不把 AOCI 的长规则复制进 MEMORY。

## 日常源码任务

```text
Kit MEMORY 首读与技术/业务门闸
  ├─ 未启用：源码＋测试核对；Kit 槽位回写；不欠 AOCI 账
  └─ 已启用且需理解/改源码：
       当前 aoci_rules → 完整 aoci_overview（按返回的 delivery_receipt_version 确认）→ 相关 Entry → 源码/测试
       → 最小代码修改与测试稳定
       → 如受管对象有变：aoci_maintain → 模型更新条目 → verify → check → Guide
       → 同轮 Kit VERIFY/ITERATION 与受影响槽位
```

读源码但没有受管对象变化时不 Maintain；纯需求/非代码任务不机械加载 AOCI。AOCI 记录“当前源码如何构成”，Kit 记录“为什么做/获批技术/阶段事实/交付”。若已启用项目的 AOCI 不可用或不对齐，允许 Kit＋源码/测试继续受限工作，但交付必须明说地图待维护，不能称闭环完成，也不能引用过时地图作权威。AOCI 不可用不等于“未启用”，不要自动改状态。

## 团队集成：源码先于全局图

个人地图是**审查提案**，不能文本合并个人 `aoci.code.txt` 或重放旧 candidate/batch/SHA。集成负责人在独立集成工作区串行纳入源码；同一对象、Scope/Meta 或证据冲突先交人工裁决。源码合并并测试稳定后，对合并后的源码重新调用当前 AOCI Maintain，由集成 Agent 按当前 Guide 撰写全局候选，再以 Verify→Check→Guide 证明对齐。只有这时提交全局地图/基线。Kit 与 AOCI 各自更新：升级 Kit 不重建地图，升级 AOCI 不自动覆盖 Skill 或宿主配置；失配时停在能力检查，不伪称闭环。

## 当前试验的交付界限

本实验只在忽略的 SSSS 快照/工作区配置 AOCI，原 SSSS 和全局 MCP 不动。工作区 TDD、真实源代码先合并后全局图维护与 Codex/Claude/Cursor 宿主日志见本实验 VERIFY。Cursor 的 `ask` 模式未暴露 MCP，普通非交互会话调用被拒，隔离 worktree 用 `-p --trust --approve-mcps --force` 才真实通过；该宽授权**不是正式项目的默认建议**。此前单沙盒 Codex 验证见 `memory/kit/annex/VERIFY-20261006-aoci-codex-session.md`。默认 Codex exec 不审批也会挡住 MCP；不能称“打开会话即自动调用”。
