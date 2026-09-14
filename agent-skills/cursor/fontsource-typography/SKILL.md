---
name: fontsource-typography
description: >-
  Self-hosts quality open fonts via Fontsource (@fontsource/*) for Vite/React/CSS.
  Use when typography looks like system default AI slop or user mentions Fontsource
  or 排版高级感.
---

# Fontsource 字体

站点：[fontsource.org](https://fontsource.org/) · npm `@fontsource/<family>`。

## 何时用

- 文档站、Dashboard、课程 HTML 需要 **稳定、可离线、无 Google Fonts 依赖** 的排版。

## 安装（示例：中文友好组合）

```bash
npm install @fontsource/inter @fontsource/noto-sans-sc
```

## 入口引用（Vite main.tsx 或 global.css）

```typescript
import '@fontsource/inter/400.css';
import '@fontsource/inter/600.css';
import '@fontsource/noto-sans-sc/400.css';
```

```css
:root {
  font-family: 'Inter', 'Noto Sans SC', system-ui, sans-serif;
}
```

## 配对建议

| 场景 | 西文 | 中文 |
| --- | --- | --- |
| 产品 UI | Inter / Geist | Noto Sans SC |
| 教程/人文 | Source Serif 4 | Noto Serif SC |

## 禁止

- 单页加载超过 4 个字重文件。
- 标题与正文用两种以上 unrelated display font。
