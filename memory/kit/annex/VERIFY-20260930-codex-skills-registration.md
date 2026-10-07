# Codex 对齐本机 Cursor 个人技能库

- 日期：2026-09-30（Asia/Shanghai）；机器：`SC-202601081030`。
- 最终授权：用户改为「看看本地的 Cursor 技能库，和他的技能一样就行」。
- 来源：`C:\Users\Administrator\.cursor\skills\`，共 22 个技能。
- 目标：`C:\Users\Administrator\.codex\skills\`。
- 结果：22 个 Cursor 个人技能全部安装，包含 227 个文件；Codex 原有 17 个目录保持不变。

## 最终范围与安装方式

直接复制本机 Cursor 个人技能库的现场内容及配套文件，未以仓内备份替代现场版本。未包含 Cursor 内置 `skills-cursor` 或插件缓存，未建立自动同步任务。

使用系统 skill-installer 的路径校验与目录复制函数。21 个技能逐文件与 Cursor 来源完全一致；`zimage-scene-image` 原文件缺少名称和用途信息，仅在 Codex 安装副本开头补齐，正文保持不变。Cursor 源文件未改。

此前按用户最初要求安装的 134 个仓库副本，已移到以下目录保存：

`C:\Users\Administrator\.codex\skill-install-backups\20260930-cursor-alignment\`

备份不在技能加载目录内。其中 22 个技能以 Cursor 现场版本重新安装，其余 112 个已撤回。移动前逐一核实绝对路径及内容，移动后核对备份完整性。

## 验证结果

| 项目 | 结果 |
| --- | --- |
| 项目记忆体量门闸 | `python scaffold/scripts/check-memory-size.py` 通过 |
| Cursor 个人技能覆盖 | 22 / 22；名称唯一，名称和用途信息可解析 |
| 安装文件逐一比对 | 227 / 227；除上述单份识别信息补齐外，与 Cursor 来源一致 |
| Cursor 源文件保留 | 所有来源目录内容校验不变 |
| 原有 Codex 技能保留 | 安装前已有 17 个目录，内容校验全部不变 |
| 最终安装目录集合 | 恰为原有 17 个目录 + Cursor 22 个目录，共 39 个；无本轮额外技能遗留 |
| 撤回备份 | 134 个最初安装副本完整保存；未删除文件 |
| 运行依赖 | 未执行各技能业务流程；个别技能仍需外部工具、服务或账号 |

新安装技能在下一轮加载。此次验证覆盖安装内容与识别信息，未把静态文件校验当成所有技能业务流程已运行通过。

本地原始清单、内容摘要和执行记录位于 `materials/_local/codex-skill-registration/`，其中最终结果为 `cursor-alignment-result.json`；按仓库约定不入库。

## 完整安装清单

以下名称在 Cursor 来源目录与 Codex 目标目录中一一对应。

| 技能名称 | 文件数 | 处理 |
| --- | --- | --- |
| `ai-agents-in-depth-zh-cn` | 14 | Exact copy |
| `anchoring-persona-memory` | 23 | Exact copy |
| `book-to-skill` | 108 | Exact copy |
| `business-context-first-agent-design` | 5 | Exact copy |
| `codebase-to-course` | 13 | Exact copy |
| `codex-premium-design-eight` | 1 | Exact copy |
| `collaboration-contract` | 2 | Exact copy |
| `compatibility-layer` | 2 | Exact copy |
| `fontsource-typography` | 1 | Exact copy |
| `github-readme-stats` | 1 | Exact copy |
| `legacy-mock-cleanup` | 2 | Exact copy |
| `markdown-badges` | 1 | Exact copy |
| `mermaid-diagrams` | 1 | Exact copy |
| `mock-collaboration` | 2 | Exact copy |
| `parallel-collaboration` | 2 | Exact copy |
| `persona-jailbreak-inject` | 1 | Exact copy |
| `project-memory-kit` | 30 | Exact copy |
| `radix-colors` | 1 | Exact copy |
| `rough-js-sketch` | 1 | Exact copy |
| `shadcn` | 14 | Exact copy |
| `simple-icons-brand` | 1 | Exact copy |
| `zimage-scene-image` | 1 | Metadata added |
