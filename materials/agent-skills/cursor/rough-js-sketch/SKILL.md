---
name: rough-js-sketch
description: >-
  Adds hand-drawn, human sketch texture using Rough.js (roughjs) on canvas/SVG.
  Use when diagrams or UI chrome look too perfect/plastic, for whiteboard-style
  explainer graphics, or when user mentions Rough.js or 手绘感.
---

# Rough.js 手绘草图

库：[roughjs](https://roughjs.com/) · npm `roughjs`。

## 何时用

- 架构示意、流程草图、课程配图需要 **故意不完美的手绘线**，对抗 AI 默认「过滑矢量/3D」。
- React/Vite 项目：优先 **SVG + roughjs** 或 canvas 导出 PNG。

## 安装

```bash
npm install roughjs
```

## 最小用法（SVG）

```javascript
import rough from 'roughjs';

const rc = rough.svg(svgElement);
rc.rectangle(10, 10, 200, 120, { fill: 'rgba(220,230,240,0.3)', roughness: 1.2, bowing: 2 });
rc.line(20, 80, 190, 80, { strokeWidth: 2 });
```

## 参数建议（设计感）

| 参数 | 建议 |
| --- | --- |
| `roughness` | 1–1.8 信息图；>2 仅装饰 |
| `bowing` | 1–3 略弯，像人手 |
| `fillStyle` | `hachure` / `cross-hatch` 比纯色更有纸感 |
| 配色 | 配合 `@radix-colors`，勿 neon |

## 禁止

- 全页 rough 纹理叠在照片上当「滤镜」。
- 与 shadcn 生产表单混在同一屏（气质冲突）。
