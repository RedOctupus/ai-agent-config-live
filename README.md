# AI Agent Configuration - Live Backup

Private backup of my Hermes Agent configuration, skills, memory, and installed tools.

**Machine:** Windows 10 workstation  
**Hermes:** v0.14.0 (DeepSeek v4 Pro)  
**Last sync:** 2026-05-24


## Cursor 个人技能备份规则

仓库：`agent-skills/cursor/`（详见 [`agent-skills/README.md`](agent-skills/README.md)）。

- **只往远程更新**：本机 `~/.cursor/skills` → 本仓库；有变化才提交推送。
- **不自动拉本机、不自动注册**：除非明确说从远端拉某个技能下来用。
- **目录**：目前一个运行时夹里平铺；成套技能放 `cursor/suites/`。以后技能多了可能再分类。
- **含 Superpowers 插件技能备份**：落到 `agent-skills/cursor/plugins/superpowers/`（来自插件缓存，不是 `~/.cursor/skills`）。
- **不含**：Cursor 内置 `skills-cursor`；其他插件默认仍不备份。

## Quick Recovery

```bash
# 1. Clone
git clone git@github.com:RedOctupus/ai-agent-config-live.git
cd ai-agent-config-live

# 2. Restore
./scripts/restore.sh

# 3. Fill in API keys
cp ~/.hermes/.env.template ~/.hermes/.env
# Edit ~/.hermes/.env

# 4. Verify
hermes doctor
hermes
```

## Structure

```
├── README.md              ← This file
├── hermes/                ← Hermes config (redacted)
│   ├── config.yaml        ← Key settings (no API keys)
│   ├── SOUL.md            ← Agent persona
│   └── .env.template      ← Required env vars
├── skills/                ← Hermes skill backup
│   └── <category>/<name>/SKILL.md
├── agent-skills/          ← 按运行时分类的个人技能（Cursor/Claude/portable）
│   └── cursor/            ← 平铺技能 + suites/ 成套技能
├── memory/                ← Persistent memory exports
│   ├── user-profile.md
│   ├── environment.md
│   └── machine.md
├── tools/                 ← Installed CLI/Agent tools catalog
│   └── catalog.md
├── scripts/               ← Sync & restore automation
│   ├── sync-skills.sh     ← Pull latest skills from Hermes
│   ├── sync-memory.sh     ← Export memory to markdown
│   └── restore.sh         ← Full disaster recovery
└── plans/                 ← Project plans
```

## Maintenance

```bash
# Sync skills after installing new ones
./scripts/sync-skills.sh

# Export latest memory
./scripts/sync-memory.sh

# Commit changes
git add -A
git commit -m "sync: YYYY-MM-DD"
git push
```

## Installed Tools

| Tool | Version | Purpose |
|---|---|---|
| Codex CLI | 0.133.0 | OpenAI autonomous coding agent |
| gh CLI | 2.92.0 | GitHub API & PR/Issue management |
| git | 2.53.0 | Version control |
| Node.js | 24.14.0 | JavaScript runtime |
| Python | 3.11.14 | Hermes venv |

## Hardware

- GPU: NVIDIA RTX 5070 Ti (16GB VRAM)
- CUDA: 13.2
