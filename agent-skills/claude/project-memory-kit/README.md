# 项目记忆包（project-memory-kit）

给**人和 Agent**用的可复用 init 包：新项目只落下少量活文档，不把整套行事哲学拷进去。

## 新项目怎么 init

1. 本机已同步到 `%USERPROFILE%\.cursor\skills\project-memory-kit\` 时，任意仓库说 `init 新项目` 即可（新开的 Cursor 窗口才一定加载得到）。
2. 否则：把治理框架加进工作区，或 `@SKILL.md`。
3. Agent 把 `templates/` 拷到目标项目：

```text
docs/memory/MEMORY.md       # 各阶段一句话快照、约束、入口
docs/memory/ENVIRONMENT.md  # 服务对象大环境
docs/memory/REQUIREMENTS.md # 需求条目
docs/memory/FRAMEWORK.md    # 项目框架
docs/memory/FLOW.md         # 实现流程
docs/memory/TODO.md
docs/memory/ITERATION.md
docs/memory/tests/_TEMPLATE.md
AGENTS.md
.cursor/rules/project-memory.mdc
```

默认**只** init 记忆目录。要 `.gitignore` / `.env.example` / `README.md` 骨架时，需另外点名「工程脚手架」。

## 希望任意仓库随口都能 init

把本目录同步到 Cursor **个人技能**（不要放进 `skills-cursor/`）：

```text
%USERPROFILE%\.cursor\skills\project-memory-kit\
```

Windows 示例：`C:\Users\Windows\.cursor\skills\project-memory-kit\`

改完治理框架里的源之后，再拷一次覆盖个人 skills，否则两套会分叉。

仍可用：把本仓库加进工作区，或对话里 `@SKILL.md`。

## 几份文档各写什么

| 文件 | 写 |
| --- | --- |
| `MEMORY.md` | **快照**：每阶段一句话 + 约束/入口。细节不写这里 |
| `ENVIRONMENT.md` | **服务对象大环境**（as-is）：服务谁、对方现在怎么办事 |
| `REQUIREMENTS.md` | **拆解条目**：可感知行为 + 验收句 + 状态 |
| `FRAMEWORK.md` | **项目框架**：技术选型（须用户逐项确认）、能力模块、分层 |
| `FLOW.md` | **实现流程**：端到端步骤、分支、每步 I/O |
| `ITERATION.md` | 变更记录 |

项目做完一版：勾 `REQUIREMENTS` 状态；改对应源文件；MEMORY 只改变了的那句快照；写 ITERATION 和测试日志。  
**只有服务对象真实办事方式变了**才改 ENVIRONMENT。不要把源文件正文堆进 MEMORY。

日常阅读规则（含 TODO、测试日志、待办、`references/`）在项目里的 `MEMORY.md` 第 5 节，**不在**这份 README 里。Skill 只负责 init 和按需打开 `references/`。
