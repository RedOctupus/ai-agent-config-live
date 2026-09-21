# Install and configure `ocr`

Skill 里**没有**审查服务。Agent 必须能在本机装上 CLI、配好（或绕过）LLM，才能跑审查。

## Prerequisites

- Git ≥ 2.41（diff / 搜索 / 仓库操作）
- Node.js ≥ 18（走 npm 安装时）
- 从源码编译时：Go ≥ 1.25、Make、Git

## Install CLI (pick one)

推荐 npm。装好后命令名是 `ocr`（Windows 上还有 `ocr.cmd`）。

### 1. npm（推荐）

```bash
npm install -g @alibaba-group/open-code-review
```

钉版本：`npm install -g @alibaba-group/open-code-review@<version>`

升级：`npm i -g @alibaba-group/open-code-review@latest`

卸载：`npm uninstall -g @alibaba-group/open-code-review`

npm 包装器默认会后台检查更新（约 18 分钟冷却，`OCR_UPDATE_INTERVAL` 单位为分钟）。关掉：`OCR_NO_UPDATE=1`。静态二进制没有这套更新。

### 2. Windows 安装脚本

```powershell
irm https://open-codereview.ai/install.ps1 | iex
```

默认目录：`%LOCALAPPDATA%\Programs\ocr`（即 `ocr.exe`）。可用环境变量：

| 变量 | 默认 | 作用 |
|------|------|------|
| `OCR_INSTALL_DIR` | `%LOCALAPPDATA%\Programs\ocr` | 安装目录 |
| `OCR_VERSION` | 最新 release tag | 钉版本，如 `v1.12.7` |
| `OCR_GITHUB_MIRROR` | 空 | 路径前缀镜像域名，例如 `gh-proxy.com`（不要带 `https://` 和末尾 `/`） |

装完若不在 PATH：把该目录加入用户 PATH，或用绝对路径调用 `ocr.exe`。

macOS / Linux 对应：

```bash
curl -fsSL https://open-codereview.ai/install.sh | sh
```

`OCR_INSTALL_DIR` 默认 `/usr/local/bin`。脚本支持 darwin/linux 的 amd64/arm64。

镜像只代理 release 二进制和 `sha256sum.txt`；解析「最新版本」仍打 GitHub API。不信任镜像时对照 https://github.com/alibaba/open-code-review/releases 上的官方 checksum。

### 3. GitHub Release 静态二进制

https://github.com/alibaba/open-code-review/releases

资源名：

- `opencodereview-windows-amd64.exe` / `opencodereview-windows-arm64.exe`
- `opencodereview-darwin-amd64` / `opencodereview-darwin-arm64`
- `opencodereview-linux-amd64` / `opencodereview-linux-arm64`
- `sha256sum.txt`

Windows 示例：把 exe 改名为 `ocr.exe` 放到已在 PATH 的目录。

### 4. Homebrew

```bash
brew install open-code-review
brew upgrade open-code-review
```

### 5. 从源码构建

仓库：https://github.com/alibaba/open-code-review.git

```bash
git clone https://github.com/alibaba/open-code-review.git
cd open-code-review
make build                 # 输出 dist/opencodereview
# Windows 交叉编译：
make build-windows-amd64
make build-windows-arm64
```

把产物放到 PATH 并命名为 `ocr` / `ocr.exe`。测试：`make test`。

## Verify

```bash
ocr version
ocr --help
ocr review --help
ocr delegate --help
```

`command not found`：查 PATH。Windows 上 npm 全局 bin 通常是 Node 安装目录或 `%APPDATA%\npm`。脚本安装默认 `%LOCALAPPDATA%\Programs\ocr`。

## LLM config（`ocr review` / `ocr scan` 需要）

Delegation **不需要** OCR 侧 LLM。

配置文件：`~/.opencodereview/config.json`（权限 0600）。

**不要**在 agent 里跑 `ocr config provider` / `ocr config model`（TUI）。用：

```bash
ocr config set provider deepseek
ocr config set model deepseek-chat
ocr config set providers.deepseek.api_key "$DEEPSEEK_API_KEY"
ocr config set language 中文
ocr llm test
```

`ocr llm providers` 列出内置 provider。常用国内项：`deepseek`、`dashscope`、`kimi`、`volcengine`、`z-ai`、`siliconflow-cn`。key 也可走对应环境变量（如 `DEEPSEEK_API_KEY`、`DASHSCOPE_API_KEY`、`MOONSHOT_API_KEY`），未写入 config 时会回退。

自定义 OpenAI 兼容网关：

```bash
ocr config set provider my-gateway
ocr config set custom_providers.my-gateway.url https://gateway.example/v1
ocr config set custom_providers.my-gateway.protocol openai
ocr config set custom_providers.my-gateway.model llama-3-70b
ocr config set custom_providers.my-gateway.api_key "$MY_API_KEY"
```

本地 Ollama：url `http://127.0.0.1:11434/v1`，protocol `openai`，`api_key` 填任意非空占位（自定义 provider 必填）。模型必须支持 native tool calling。

连通性：`ocr llm test`。`no valid LLM endpoint configured` = 没配好；401/403 = token 错或过期。**永远不要编造 key。**

## Cursor plugin（可选）

CLI 与 plugin 是两件事。Plugin 只把官方 skill 暴露给 Cursor，**代替不了 `ocr` 二进制**。

手动安装：把仓库里的 `plugins/open-code-review/` **整目录**拷到：

```text
~/.cursor/plugins/local/open-code-review/
```

检查存在：`~/.cursor/plugins/local/open-code-review/.cursor-plugin/plugin.json`（其中 `"skills": "../skills/"` 指向同目录下 `skills/`）。然后 **Developer: Reload Window**。需允许本地 plugin。

官方说明：仓库 `plugins/open-code-review/README.md` 的 Cursor 节。

也可用：`npx skills add alibaba/open-code-review --skill open-code-review`（以及 `--skill open-code-review-delegate`）。那是项目内 skill 拷贝，同样要求本机已有 `ocr`。

## State directories

| 路径 | 内容 |
|------|------|
| `~/.opencodereview/config.json` | LLM、language、telemetry |
| `~/.opencodereview/rule.json` | 全局规则 |
| `~/.opencodereview/sessions/` | 会话 JSONL（`ocr viewer` / `--resume`） |
| `<repo>/.opencodereview/rule.json` | 项目规则，可提交 |

删掉 `~/.opencodereview/` 即清配置（不含卸载二进制）。

## Agent bootstrap

不要从这里擅自开始装。先跑 `scripts/check-env.ps1`（Unix：`scripts/check-env.sh`），再按 JSON `next` 走 [init.md](init.md)。

1. `init-install`：AskQuestion 让用户选安装方式（推荐项来自 JSON `recommend.install`），再执行对应命令。
2. 装完把 npm 全局 bin 或 `OCR_INSTALL_DIR` 加入 **当前 shell** PATH，再体检。
3. GitHub 下载失败：问用户是否设 `OCR_GITHUB_MIRROR`（路径前缀镜像）或改 npm。
4. `init-llm`：AskQuestion 选 OCR API 或委托；key 只用 `ocr config set`，然后 `ocr llm test`。
5. 通过后跑 `scripts/start-viewer.ps1`，再调度审查。
