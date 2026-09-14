---
name: codex-premium-design-eight
description: >-
  Orchestrates the eight-tool “高级设计感” stack (Rough.js, shadcn/ui, Radix Colors,
  README Stats, Mermaid, Simple Icons, Fontsource, Markdown Badges) to reduce AI
  “塑料感”. Use when the user asks for Codex/Cursor design物料、README 美化、手绘信息图、
  品牌感 UI、或引用小红书「Codex 必装高级设计感 Skill」清单。
---

# Codex 高级设计感 · 八件套

笔记来源：小红书「Codex 必装高级设计感 Skill」（作者：小胖的AI踩坑日记）。  
**说明**：其中多数是 **npm/开源库 + 用法规范**，不是八个独立 GitHub Skill 仓库；本目录把其注册为 Cursor 可 `@` 的子技能。

## 组合顺序（默认）

1. **定气质**：`rough-js-sketch` 或 `mermaid-diagrams`（结构/手绘）
2. **定配色**：`radix-colors`（禁止随机 hex 堆砌）
3. **定排版**：`fontsource-typography`
4. **定组件**：`shadcn`（有 `components.json` 的项目）
5. **定图标**：`simple-icons-brand`
6. **定 README 装饰**：`markdown-badges` + `github-readme-stats`

## 子技能路径（个人目录）

| 用途 | 文件夹 |
| --- | --- |
| 手绘草图感 | `~/.cursor/skills/rough-js-sketch` |
| 组件 UI | `~/.cursor/skills/shadcn` |
| 高级配色 | `~/.cursor/skills/radix-colors` |
| GitHub 统计卡片 | `~/.cursor/skills/github-readme-stats` |
| 流程/架构图 | `~/.cursor/skills/mermaid-diagrams` |
| 品牌图标 | `~/.cursor/skills/simple-icons-brand` |
| 自托管字体 | `~/.cursor/skills/fontsource-typography` |
| Shields 徽章 | `~/.cursor/skills/markdown-badges` |

## 反塑料 checklist

- 不用「科技感、未来感、蓝紫渐变、发光线条」等空形容词当唯一 prompt。
- 每个视觉元素要能回答：**服务哪段正文、表达什么关系**。
- 同一文档/页面内 **一种主风格**（手绘 / 扁平信息卡 / shadcn 语义色），不要混 3D + 霓虹 + 手绘。

## 零基础优先（与笔记评论一致）

先 `@rough-js-sketch` + `@radix-colors`，再按需加其余技能。
