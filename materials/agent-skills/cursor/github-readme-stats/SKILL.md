---
name: github-readme-stats
description: >-
  Embeds dynamic GitHub profile/repo stat cards (github-readme-stats) in README
  and docs. Use when beautifying GitHub README, portfolio badges, or 动态可视化卡片.
---

# GitHub README Stats

项目：[anuraghazra/github-readme-stats](https://github.com/anuraghazra/github-readme-stats)（通过 shields 风格 URL 嵌入，无需本地跑服务）。

## 常用卡片 URL

**用户统计**

```markdown
![Stats](https://github-readme-stats.vercel.app/api?username=YOUR_USER&show_icons=true&theme=default&hide_border=true)
```

**仓库语言**

```markdown
![Top Langs](https://github-readme-stats.vercel.app/api/top-langs/?username=YOUR_USER&layout=compact&theme=default)
```

**单仓库**

```markdown
![Repo Card](https://github-readme-stats.vercel.app/api/pin/?username=ORG&repo=REPO&theme=default)
```

## 主题

`theme=` 可选 `default`, `dark`, `radical`, `merko`, `gruvbox`, `tokyonight` 等。  
与 `@radix-colors` 对齐时优先 **低饱和 theme**（`default` / `gruvbox`），避免 `radical` 霓虹感。

## 注意

- 公共实例有 rate limit；企业 README 可自托管 vercel 或 Docker。
- 卡片是 **装饰 + 信息**，不能替代项目说明正文。
