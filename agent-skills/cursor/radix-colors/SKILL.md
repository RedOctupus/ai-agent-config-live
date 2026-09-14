---
name: radix-colors
description: >-
  Applies Radix Colors scales (12-step, accessible) for UI and docs instead of
  random Tailwind defaults. Use when picking palettes, theming, or avoiding
  AI-blue-purple gradient slop; pairs with shadcn semantic tokens.
---

# Radix Colors 配色

站点：[radix-ui.com/colors](https://www.radix-ui.com/colors) · npm `@radix-ui/colors`。

## 何时用

- 新页面/文档/信息卡需要 **一套完整灰阶 + 主色 + 语义色**（success/warning/error）。
- shadcn 项目：把 Radix scale 映射到 CSS 变量，而不是 `bg-blue-500`。

## 安装

```bash
npm install @radix-ui/colors
```

## CSS 变量模式（Vite/React）

```css
@import '@radix-ui/colors/slate.css';
@import '@radix-ui/colors/indigo.css';

:root {
  --background: var(--slate-1);
  --foreground: var(--slate-12);
  --primary: var(--indigo-9);
  --primary-foreground: white;
}
```

## 选型

| 场景 | 推荐 scale |
| --- | --- |
| 金融/企业后台 | `slate` + `indigo` 或 `blue` |
| 温暖教程/课程 | `sand` + `orange` 或 `grass` |
| 深色模式 | 同一 scale 的 dark 变体，勿手调对比度 |

## 禁止

- 同一屏 4 种以上 accent scale。
- 用 `#3b82f6` 等硬编码覆盖已定义的 semantic token。
