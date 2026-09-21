# AI Agent Configuration - Live Backup

Private backup of my Hermes Agent configuration, skills, memory, and installed tools.

**Machine:** Windows 10 workstation  
**Hermes:** v0.14.0 (DeepSeek v4 Pro)  
**Last sync:** 2026-05-24


## Cursor 个人技能备份规则

仓库：`materials/agent-skills/cursor/`（详见 [`materials/agent-skills/README.md`](materials/agent-skills/README.md)）。

- **只往远程更新**：本机 `~/.cursor/skills` → 本仓库；有变化才提交推送。
- **不自动拉本机、不自动注册**：除非明确说从远端拉某个技能下来用。
- **目录**：目前一个运行时夹里平铺；成套技能放 `cursor/suites/`。以后技能多了可能再分类。
- **含 Superpowers 插件技能备份**：落到 `materials/agent-skills/cursor/plugins/superpowers/`（来自插件缓存，不是 `~/.cursor/skills`）。
- **不含**：Cursor 内置 `skills-cursor`；其他插件默认仍不备份。

## Quick Recovery

```bash
# 1. Clone
git clone git@github.com:RedOctupus/ai-agent-config-live.git
cd ai-agent-config-live

# 2. Restore
./scaffold/scripts/restore.sh

# 3. Fill in API keys
cp ~/.hermes/.env.template ~/.hermes/.env
# Edit ~/.hermes/.env

# 4. Verify
hermes doctor
hermes
```

## Structure

三层分开存放，根目录只留入口文档与 Cursor 规则：

```
├── README.md / AGENTS.md / .gitignore / .cursor/rules/
├── scaffold/                 ← 脚手架（同步、恢复、体量门闸）
│   └── scripts/
│       ├── sync-skills.sh
│       ├── sync-memory.sh
│       ├── restore.sh
│       ├── auto-sync.sh
│       └── check-memory-size.py
├── memory/                   ← 记忆（两套，不要混）
│   ├── kit/                  ← 本仓 project-memory-kit（日常只读 MEMORY.md）
│   └── hermes/               ← Hermes 长期记忆导出
└── materials/                ← 本地物料（技能、配置、清单、计划）
    ├── hermes/               ← Hermes 配置（脱敏；无 API keys）
    ├── skills/               ← Hermes 技能备份
    ├── agent-skills/         ← Cursor / Claude / portable 个人技能
    ├── tools/                ← CLI/Agent 工具清单
    ├── plans/                ← 历史计划
    └── _local/               ← 本机临时物料（git 忽略）
```

其他项目里 kit 默认仍是 `docs/memory/`；**只有本仓**把 kit 记忆放在 `memory/kit/`，以免和 Hermes 导出抢根目录 `memory/`。

## Maintenance

```bash
# Sync skills after installing new ones
./scaffold/scripts/sync-skills.sh

# Export latest Hermes memory → memory/hermes/
./scaffold/scripts/sync-memory.sh

# This repo's kit size gate
python scaffold/scripts/check-memory-size.py

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
