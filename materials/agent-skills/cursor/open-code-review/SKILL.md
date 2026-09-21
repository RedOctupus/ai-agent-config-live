---
name: open-code-review
description: >-
  Use when the user asks to review code, a PR, staged/unstaged/untracked
  changes, a commit, or a branch range with Open Code Review / ocr; also when
  ocr is missing, the review environment is unconfigured, init is needed,
  or the OCR viewer/service must be started for alibaba/open-code-review;
  also when deploying OCR onto GitHub Actions / CI/CD, PR auto-review,
  or copying the upstream GitHub Action.
---

# Open Code Review

`ocr` 是独立 CLI，审查引擎不在 skill 包里。每次调用按下面 **Gate** 顺序走：体检 → 必要时 init → 打开 viewer → 再调度 `ocr review` / `scan` / `delegate`。

安装细节：[install.md](install.md)。Init 问答：[init.md](init.md)。

官方仓库：https://github.com/alibaba/open-code-review  
NPM：https://www.npmjs.com/package/@alibaba-group/open-code-review  
CI/CD（GitHub Actions 等）：[cicd.md](cicd.md) — 有官方 Action，**不要**现编 workflow。

## When to use

- 审工作区改动、PR、commit、分支 diff，或全量 `ocr scan`
- 点名 Open Code Review / OCR / `ocr` / 委托模式 / viewer
- 环境没配好、要安装、要填大模型 API
- 要把 OCR **部署到 GitHub Actions / CI**、PR 自动审查、评论触发再审

**不要用：** 用户只要改代码、不要审查结果；或只要跑 ESLint/单测。

**CI/CD 与本机审查分流：** 用户只要 GitHub / CI 自动审 PR → **REQUIRED** 打开 [cicd.md](cicd.md)，按指针读上游，**不要**走下面 Gate、不要本机 `ocr review`。只有同时还要在本机审，才走 Gate。

## Gate（每次第一件事）

**固定顺序，四步都要留下可观察结果。** 不要先 `git diff`、不要先 `ocr review`、不要因为「上次能跑」而跳过。

1. 跑体检脚本（本 `SKILL.md` 同目录）：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check-env.ps1
```

```bash
bash scripts/check-env.sh
```

读 JSON 的 `next` / `missing` / `recommend` / `ready_for` / `viewer`。脚本 **不会打印 API key**。

2. `next` 为 `init-git` / `init-install` / `init-llm` → **REQUIRED：** 打开 [init.md](init.md)，按 `next` 做完，再跑一遍 check-env。未通过前禁止审查。
3. `next` 为 `start-viewer` 或 `dispatch` → 打开 viewer（下节），再调度审查。
4. 只有 `ready_for` 含 `review` 才能 `ocr review` / `ocr scan`。只有 `delegate` 时走委托，或先走 init-llm。

| 借口 | 实际 |
|------|------|
| 「省一次探测」 | 用户要求先体检。脚本很快。 |
| 「大概装过了」 | 以 JSON `ocr.ok` 为准。 |
| 「没装就自己 git diff 审」 | 漏文件、行号漂。先 init-install。 |
| 「没 API 就编一个 / 开 TUI」 | 走 init-llm 或 delegate。 |
| 「先出审查结果再补环境」 | 顺序反了。Gate 在前。 |

**Red flags：** 第一条命令是 `git status` / `git diff` / `ocr review`；跳过 AskQuestion 擅自选安装方式；`ocr config provider`。

## Start viewer（调度用的本地服务）

OCR 没有独立审查守护进程。可长期开着的是会话 WebUI（默认 `localhost:5483`），审查任务仍用 CLI 调度。

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/start-viewer.ps1
```

```bash
bash scripts/start-viewer.sh
```

- JSON `already_running: true` → 复用，不要再起一份。
- 用 `--open=never`，不要抢用户浏览器（脚本已带）。
- 告诉用户 URL（一般 `http://localhost:5483`），然后立刻调度审查，不要空等 WebUI。

## Hard rules

1. **审查走 `ocr`，不要自己读完 `git diff` 当审查。**
2. **禁止发明 flag。** 不确定就 `ocr review --help` / `ocr delegate --help`。
3. **永远不要编造或写入 API key 到 git/skill。** 无 TTY：`ocr config set`。
4. **Agent 调用必须带 `--audience agent`。**
5. **结果写入文件再 Read。** Windows：`--format json --output $env:TEMP\ocr_out.json`。禁止 `head`/`tail`/`-First`。
6. **有业务上下文就传 `--background`（或 `--background-file`）。**
7. **只 review、没说 fix：先问再改代码。** 「review and fix / 审完并修」才改 critical/high/medium。

## Mode selection

Gate 通过之后：

```
用户要全量扫文件 / 无有效 diff / 审陌生目录？
  → ocr scan ...（需要 ready_for 含 scan）
否则 ready_for 不含 review，或用户说 delegate / 用 Cursor 自己审？
  → Delegation
否则
  → ocr review ...
```

`ocr review` 因 LLM 连接失败：不要重试乱填 key。再跑 `check-env.ps1 -TestLlm`，然后 init-llm 或改委托。

## Fake flags

| 不要写 | 实际 |
|--------|------|
| `--uncommitted` | 默认工作区：staged + unstaged + untracked |
| `--base main` | `--from main --to <branch>` |
| `--dry-run` | `--preview` / `-p` |
| `--quick` / `--lite` | `--effort low` |
| `--verbose` | `--audience agent` |
| `git diff \| ocr review` | `ocr` 自己读仓库；`--repo` 指定根目录 |

## OCR-managed review

```bash
ocr review --audience agent --background "一句话业务背景" --format json --output "$OCR_OUT" [范围]
```

Windows：`$OCR_OUT` = `$env:TEMP\ocr_out.json`。

| 用户说 | 范围参数 |
|--------|----------|
| 当前改动 / working copy | （不加范围） |
| 这个 PR / feature 相对 main | `--from main --to <branch>` |
| 某次 commit | `--commit <hash>` |
| 先看会审哪些文件 | `--preview` |
| 中断后续跑 | `--resume <session-id>`（`ocr session list`；工作区模式不能 resume） |

超时：`--timeout`（默认 15 分钟）× effort 轮数（low/medium/high = 1/2/3）。并发默认 8。

`unknown flag: --output` → CLI 低于 v1.10.0。先问是否 `npm i -g @alibaba-group/open-code-review@latest`。

## Delegation

1. `ocr delegate preview --format json`
2. `ocr delegate rule --format json <path1> <path2> ...`
3. range：`git diff <merge_base>..<to> -- <path>`；commit：`git show <commit> -- <path>`；workspace 已跟踪：`git diff HEAD -- <path>`；未跟踪：读文件
4. 每个 `reviewable_files` 标 `reviewed` 或 `skipped`（带原因）。身份是 `(path, status)`
5. 汇总：`total_files` / `reviewed_files` / `skipped_files` / `coverage_rate`

`unknown flag: --format` → CLI 低于 v1.9.0：去掉 flag 用文本，不要当 JSON 解析。

`--background-file` 超 1 MiB 或清洗后超 8000 字符：不要截断原文件；改短摘要作 `-b`，去掉原来的 `--background-file`。

## Full-file scan

```bash
ocr scan --audience agent --background "..." --format json --output "$OCR_OUT"
ocr scan --path internal/agent --preview
ocr scan --resume <session-id>
```

## Report

丢弃明显误报和 **low**。`start_line` 与 `end_line` 都是 `0`：读 `content`，打开 `path`，对上代码再报。

```markdown
## Code Review Results

**Files reviewed**: N
**Issues found**: X critical, Y high, Z medium

### Critical
- **`path/file.go:42`** [bug] — 一句话
  > Recommendation: 怎么改
```

无 critical/high/medium：`Review complete — no critical, high, or medium issues found in N files.`

## Custom rules

`--rule` → `<repo>/.opencodereview/rule.json` → `~/.opencodereview/rule.json` → 内置。叠加：`merge_system_rule: true`。预览：`ocr rules check <file>`。

## Additional resources

- Init 问答：[init.md](init.md)
- 安装与配模型：[install.md](install.md)
- GitHub Actions / CI 部署指针：[cicd.md](cicd.md)
- 体检 / 启 viewer：`scripts/check-env.ps1`、`scripts/start-viewer.ps1`（Unix 用对应 `.sh`）
