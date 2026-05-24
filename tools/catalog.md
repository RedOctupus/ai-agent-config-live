# Tools Catalog

> All installed CLI and Agent tools on this machine. Updated: 2026-05-24

## AI Agent Tools

### Codex CLI (OpenAI)
- **Version:** 0.133.0
- **Install:** `npm install -g @openai/codex`
- **Auth:** `codex login` (browser OAuth with OpenAI Pro)
- **Model:** gpt-5.5
- **Usage patterns:**
  ```bash
  # One-shot task
  codex exec "build a FastAPI endpoint for user auth"

  # Sandbox writable (recommended)
  codex exec --sandbox workspace-write "refactor src/auth/"

  # Full auto (no approvals)
  codex --yolo exec "fix all eslint warnings"

  # PR review
  codex review
  ```
- **Requirements:** Must run inside a git repo
- **Deprecated:** `--full-auto` → use `--sandbox workspace-write`

### Hermes Agent
- **Version:** 0.14.0
- **Install:** `curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash`
- **Provider:** DeepSeek (deepseek-v4-pro)
- **Key commands:**
  ```bash
  hermes                    # Interactive chat
  hermes chat -q "prompt"   # Single query
  hermes model              # Change model/provider
  hermes config edit        # Edit config
  hermes tools              # Manage toolsets
  hermes skills list        # List installed skills
  hermes doctor             # Health check
  hermes setup              # Setup wizard
  ```

## Development Tools

### Git
- **Version:** 2.53.0
- **Shell:** Git Bash (MSYS), NOT PowerShell or cmd
- **Note:** Always use POSIX syntax (`ls`, `$HOME`, `&&`, `|`)

### GitHub CLI
- **Version:** 2.92.0
- **Path:** `C:\Program Files\GitHub CLI\gh.exe`
- **Auth:** `gh auth login` (browser OAuth)
- **Key commands:**
  ```bash
  gh auth status            # Check auth
  gh repo list              # List repos
  gh pr create              # Create PR
  gh issue list             # List issues
  gh api <endpoint>         # Raw API call
  ```

### Node.js
- **Version:** 24.14.0 LTS
- **Package manager:** npm 11.9.0, uv 0.10.2

### Python
- **Hermes venv:** 3.11.14 at `D:\09-其他\hermes-agent\venv\`
- **System:** 3.13.9
- **Package manager:** uv 0.10.2

### Windows Package Manager
- **winget:** 1.28
- **Usage:** `winget install <id>`, `winget list`

## GPU / ML Tools

| Tool | Version |
|---|---|
| NVIDIA Driver | 596.49 |
| CUDA Toolkit | 13.1 |
| CUDA (driver) | 13.2 |
| cuDNN | Via CUDA toolkit |
| Nsight Compute | 2025.4.1 |
| Nsight Systems | 2025.5.2 |
