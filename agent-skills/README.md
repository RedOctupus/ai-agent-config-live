# Agent skills（按运行时分类）

私人备份：本机个人技能按 Agent 分夹。不含 Cursor 内置技能（`~/.cursor/skills-cursor`）。

```text
agent-skills/
  portable/   不绑特定产品。能读 SKILL.md 的 Agent / 自建 Harness 整夹拷走即可
  cursor/     本机 ~/.cursor/skills + 叙境仓库 .cursor/skills
  claude/     本机 ~/.claude/skills
```

## 安装

**Cursor：** 把 `cursor/<name>/` 拷到 `~/.cursor/skills/<name>/`。  
**Claude Code：** 把 `claude/<name>/` 拷到 `~/.claude/skills/<name>/`。  
**其他 Agent：** 优先用 `portable/`。把目录交给该运行时的 skills 加载方式，或把 `SKILL.md` 当系统/项目说明读入。

## `anchoring-persona-memory` 能不能给非 Cursor 用？

能。它是 Markdown 方法 + 空模板，不依赖 Cursor API。

宿主仍要：

1. 能在使用者看见之前拦截可见输出  
2. 模型有 thinking / reasoning 通道  

缺一就换框架或换模型。Cursor 只是本机的一份安装位置。

## 本批清单

| 夹 | 技能 |
|---|---|
| portable | anchoring-persona-memory |
| cursor | anchoring-persona-memory, book-to-skill, ai-agents-in-depth-zh-cn, project-memory-kit, persona-jailbreak-inject, zimage-scene-image |
| claude | canvas-design, notebook-tutor, task-framework, code-example, temp-literature-search, project-memory-kit |
