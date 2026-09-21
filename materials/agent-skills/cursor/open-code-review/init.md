# Init protocol

`scripts/check-env.*` 的 `next` 不是 `start-viewer` / `dispatch` 时走这里。问用户用 **AskQuestion**（没有该工具就按同样选项口头问）。**一次只问一题**，用脚本 JSON 里的 `recommend.*` 给「Recommended」。

禁止：`ocr config provider` / `ocr config model`（TUI）；编造 API key；把 key 写进 skill、仓库、聊天总结。

## init-git

告诉用户：需要 Git ≥ 2.41。给安装入口 https://git-scm.com/download/win （Windows）或本机包管理器。装完请用户开新终端或确认 PATH 后，再跑 check-env。在此之前不要装 ocr、不要审查。

## init-install

AskQuestion：

- id: `install_method`
- prompt: `本机没有可用的 ocr CLI。选一种安装方式。`
- 选项（把 JSON `recommend.install` 那一项标 Recommended，并在 prompt 里带上 `recommend.install_reason`）:
  - `npm` — `npm install -g @alibaba-group/open-code-review`（有 Node 18+ 时默认推荐）
  - `windows-ps1` — `irm https://open-codereview.ai/install.ps1 | iex`
  - `install-sh` — `curl -fsSL https://open-codereview.ai/install.sh | sh`（macOS/Linux）
  - `github-binary` — 从 https://github.com/alibaba/open-code-review/releases 下对应 `opencodereview-*`
  - `homebrew` — `brew install open-code-review`
  - `source` — clone 后 `make build`（要 Go ≥ 1.25）

命令细节见 [install.md](install.md)。用户选定后 **立刻执行**，不要改用未选中的方式。

GitHub 下载失败：先问可否设 `OCR_GITHUB_MIRROR`（例如 `gh-proxy.com`，不要带 `https://`），或改 npm。

装完：把 npm 全局 bin 或 `%LOCALAPPDATA%\Programs\ocr` 加入 **当前 shell** PATH（若 `ocr` 仍找不到），再跑 check-env。

## init-llm

此时 `ocr` 已可用，但 OCR 侧 LLM 未配置。`ocr review` / `ocr scan` 会失败；`ocr delegate` 可以跑。

AskQuestion：

- id: `engine`
- prompt: `OCR 命令行已装好。审查用哪套模型？`
- 选项:
  - `ocr-llm`（若 `recommend.provider` 有现成 env，标 Recommended）— OCR 自己调 API（`ocr review` / `ocr scan`）
  - `delegate` — 不配 OCR API，用 Cursor 当前模型审（`ocr delegate`）

### 选 `delegate`

`ocr config set language 中文`（若用户要中文评论；委托模式评论语言由宿主模型决定，这条主要给以后的 `ocr review` 预留）。然后 `next` 视为 `start-viewer`。不要向用户要 key。

### 选 `ocr-llm`

1. AskQuestion `provider`：`deepseek` / `dashscope` / `kimi` / `openai` / `anthropic` / `custom`。把 `recommend.provider` 标 Recommended，prompt 附 `recommend.provider_reason`。
2. 请用户在聊天里发送 API key（或说「用已经导出的环境变量 xxx」）。**不要编造。**
3. 默认模型（用户没另说就用）:

| provider | model |
|----------|--------|
| deepseek | `deepseek-chat` |
| dashscope | `qwen-plus` |
| kimi | `kimi-k2-0905-preview` |
| openai | `gpt-4.1` |
| anthropic | `claude-opus-4-6` |

自定义网关：再要 `url`、`protocol`（`openai` / `anthropic` / `openai-responses`）、`model`。

4. 非交互写入（PowerShell 用 `$env:...`，不要 `echo` key）：

```bash
ocr config set provider deepseek
ocr config set providers.deepseek.api_key "$DEEPSEEK_API_KEY"
ocr config set language 中文
```

自定义：

```bash
ocr config set provider my-gateway
ocr config set custom_providers.my-gateway.url https://gateway.example/v1
ocr config set custom_providers.my-gateway.protocol openai
ocr config set custom_providers.my-gateway.model llama-3-70b
ocr config set custom_providers.my-gateway.api_key "$MY_API_KEY"
```

5. `ocr llm test`。成功再跑 check-env。401/403 → 请用户换 key，不要换没选过的 provider 瞎试。

内置 provider 全表：`ocr llm providers`。环境变量回退见 [install.md](install.md)。

## 完成后

check-env 的 `next` 为 `start-viewer` 或 `dispatch` 后，回到 SKILL.md 的「Start viewer」再调度审查。
