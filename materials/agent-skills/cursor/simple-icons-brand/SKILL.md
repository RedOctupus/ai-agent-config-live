---
name: simple-icons-brand
description: >-
  Uses Simple Icons for consistent brand logos (React simple-icons or SVG CDN).
  Use in README, landing pages, and docs when needing GitHub/NPM/品牌 logo without
  mismatched icon packs.
---

# Simple Icons 品牌图标

站点：[simpleicons.org](https://simpleicons.org/) · npm `simple-icons` · React `@icons-pack/react-simple-icons`。

## 何时用

- README 技术栈行、Footer「Built with」、课程页品牌条。

## React（Vite）

```bash
npm install @icons-pack/react-simple-icons
```

```tsx
import { SiReact, SiTypescript } from '@icons-pack/react-simple-icons';

<SiReact color="#61DAFB" size={24} title="React" />
```

## Markdown / 静态 HTML

官方 SVG CDN（注意 slug 与品牌色）：

```html
<img src="https://cdn.simpleicons.org/react/61DAFB" alt="React" width="24" height="24" />
```

## 规范

- 尺寸统一（16/20/24），与 `@fontsource-typography` 行高对齐。
- 使用 **官方 brand hex**（simpleicons 页面可查），勿随机改色除非品牌允许。

## 禁止

- 混用 Font Awesome + Simple Icons 同一工具栏。
- 无授权的商标大图当 hero 背景。
