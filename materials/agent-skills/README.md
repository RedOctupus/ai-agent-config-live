# Agent skills（按运行时分类）

私人备份：本机个人技能按 Agent 分夹。不含 Cursor 内置技能（`~/.cursor/skills-cursor`）。也不含 Cursor 插件技能（如 superpowers 插件缓存）。

```text
agent-skills/
  portable/   不绑特定产品。能读 SKILL.md 的 Agent / 自建 Harness 整夹拷走即可
  cursor/     Cursor 个人技能备份（见下方同步规则）
  claude/     本机 ~/.claude/skills
  codex/      Codex 协调技能与原创建工具源码；MCP 显式配置
```

## Cursor 同步规则（重要）

1. **只往远程更新**：本机 `~/.cursor/skills` → 本仓库 `materials/agent-skills/cursor/`。有新技能或内容变更才 commit/push。
2. **不自动拉本机、不自动注册**：除非明确说「从远端拉某某技能下来用」，否则不要把仓库里的技能拷进 `~/.cursor/skills`，也不要替本机注册/启用。
3. **目录形态**：目前个人技能主要平铺在 `cursor/<name>/`；成套技能放进 `cursor/suites/<suite-name>/`。技能多了以后会再按主题分类，不必永远平铺。
4. **Superpowers 插件**：也纳入定时备份。来源是本机 `~/.cursor/plugins/cache/cursor-public/superpowers/<hash>/skills`，远端落在 `cursor/plugins/superpowers/`。这是插件技能备份，不等于自动重装插件；恢复方式以 Cursor 插件安装为准，除非另有说明。
5. **双机**：家里台式机 `SC-202601081030` 与学校笔记本 `DESKTOP-DKO2LI9` 的个人 skills（及上述 Superpowers）合并上传；冲突取较新，拿不准偏台式机。

## 安装（仅在明确要求时）

**Cursor：** 把对应目录拷到 `~/.cursor/skills/<name>/`（套件则从 `cursor/suites/.../<name>/` 取）。  
**Claude Code：** 把 `claude/<name>/` 拷到 `~/.claude/skills/<name>/`。  
**其他 Agent：** 优先用 `portable/`。

**Codex Cursor CLI Controller（0.1.0）：** 源码在 `codex/cursor-cli-controller/`，MCP、Python/CLI 前置、Kit 检测、独立审计与署名约定见 [工具介绍](../tools/cursor-controller/README.md)。仓根运行 `python scaffold/scripts/install-cursor-controller.py verify` 检查来源完整性；安装/配置默认预览，显式 `--apply` 写入。相同内容可复用，已有不同源码或同名服务配置停止并留给明确更新；不向 Cursor 反向安装调度器。

**Project Memory Kit（v1.7.1）：** 两份权威副本一致；用户明确要求安装/更新时，在仓根运行 `python scaffold/scripts/install-memory-tools.py install --component kit --apply`，同时更新 Codex `~/.agents/skills`、Claude Code、Cursor 的 Kit，并备份旧副本。配套 AOCI 官方发布包和项目级 MCP 配置入口见 [仓内分发](../tools/aoci/README.md)；Kit/AOCI 分别更新，日常备份的单向规则不变。

## `anchoring-persona-memory` 能不能给非 Cursor 用？

能。它是 Markdown 方法 + 空模板，不依赖 Cursor API。

宿主仍要：

1. 能在使用者看见之前拦截可见输出  
2. 模型有 thinking / reasoning 通道  

缺一就换框架或换模型。Cursor 只是本机的一份安装位置。

## 本批清单

| 夹 | 技能 |
|---|---|
| portable | anchoring-persona-memory, business-context-first-agent-design, agent-memory-design |
| codex | cursor-cli-controller（0.1.0；原创建 Skill + 本地任务 MCP，同一源码） |
| cursor（平铺） | anchoring-persona-memory, business-context-first-agent-design, book-to-skill, ai-agents-in-depth-zh-cn, ai-finance-dev-guide, deepeval, project-memory-kit, persona-jailbreak-inject, zimage-scene-image, codebase-to-course, open-code-review |
| cursor/suites/parallel-collaboration | parallel-collaboration（总控）, collaboration-contract, compatibility-layer, mock-collaboration, legacy-mock-cleanup |
| cursor/plugins/superpowers | Superpowers 插件 skills（brainstorming、tdd、writing-plans 等） |
| claude | business-context-first-agent-design, canvas-design, notebook-tutor, task-framework, code-example, temp-literature-search, project-memory-kit |
