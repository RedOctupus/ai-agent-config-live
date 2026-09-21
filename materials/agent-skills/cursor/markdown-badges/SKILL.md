---
name: markdown-badges
description: >-
  Composes Shields.io / markdown badge rows for README and docs (build, license,
  version). Use with github-readme-stats for polished repo headers; references
  Ileriayo/markdown-badges patterns.
---

# Markdown Badges（Shields）

参考集合：[Ileriayo/markdown-badges](https://github.com/Ileriayo/markdown-badges) · 引擎 [shields.io](https://shields.io/)。

## 何时用

- README 顶栏：CI、覆盖率、license、PyPI/npm version、文档链接。

## 模板

```markdown
[![Tests](https://img.shields.io/github/actions/workflow/status/ORG/REPO/ci.yml?style=flat-square)](https://github.com/ORG/REPO/actions)
[![License](https://img.shields.io/github/license/ORG/REPO?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue?style=flat-square&logo=python&logoColor=white)]()
```

## 样式

- 统一 `style=flat-square` 或 `for-the-badge` **二选一**，不要混排。
- logo 用 `logo=` 时优先 Simple Icons 在 shields 支持的名称。

## 与 README Stats 分工

| 工具 | 作用 |
| --- | --- |
| markdown-badges | 短标签、链接、版本 |
| github-readme-stats | 大卡片、统计图 |

## 禁止

- 一行 12 个徽章「徽章墙」无信息层次。
- 伪造 build passing / coverage 数字。
