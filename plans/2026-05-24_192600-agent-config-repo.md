# Plan: Agent Configuration Backup Repository

**Created:** 2026-05-24 19:26 CST
**Repo:** RedOctupus/ai-agent-config-live (private, already exists)
**Goal:** Turn the existing private repo into a living backup of Hermes skills, long-term memory, and installed Agent/CLI tools on this machine.

---

## 1. Context

### Machine State

| Category | Detail |
|---|---|
| OS | Windows 10, git-bash (MSYS) shell |
| GPU | NVIDIA RTX 5070 Ti, 16GB VRAM, CUDA 13.2 |
| Hermes | v0.14.0, installed at `D:\09-其他\hermes-agent\` |
| Python | 3.11.14 (Hermes venv), 3.13.9 (system) |
| Node.js | 24.14.0 LTS |
| Config | Provider: deepseek, model: deepseek-v4-pro, max_turns: 90 |
| Persona | Default (SOUL.md exists but is empty/comment-only) |

### Installed AGENT TOOLS

| Tool | Version | How Called |
|---|---|---|
| Codex CLI | 0.133.0 | `terminal(codex exec ..., pty=true)` |
| gh CLI | 2.92.0 | `"/c/Program Files/GitHub CLI/gh.exe"` |
| git | 2.53.0 | native |
| winget | 1.28 | package manager |

### Installed Skills

89 skills across 16+ categories. Key categories: autonomous-ai-agents, creative, data-science, devops, github, mlops, productivity, software-development, research.

### Memory Store

Currently 1 entry (GitHub setup info). Located at `~/.hermes/memories/`.

---

## 2. Repo Structure Plan

The repo already exists as `RedOctupus/ai-agent-config-live` (private). We will populate it with this structure:

```
ai-agent-config-live/
├── README.md                  # Overview + quick recovery guide
├── hermes/
│   ├── config.yaml            # Redacted config (no API keys)
│   ├── SOUL.md                # Current persona
│   └── .env.template          # Env var template (no secrets)
├── skills/
│   ├── manifest.md            # Full skill list with descriptions (index)
│   ├── autonomous-ai-agents/  # All 89 skills, full content
│   ├── creative/              #   SKILL.md + references/ + templates/
│   ├── github/                #   Mirrors ~/.hermes/skills/ layout
│   ├── mlops/                 #   Complete, self-contained backup
│   ├── software-development/  #   Restore-ready
│   └── ...                    #   (all 16+ categories)
├── memory/
│   ├── user-profile.md        # User preferences, identity
│   └── environment.md         # Machine environment facts
├── tools/
│   ├── catalog.md             # All installed CLIs + agent tools
│   ├── codex.md               # Codex CLI setup & usage notes
│   ├── github.md              # gh CLI auth & workflow notes
│   └── hermes.md              # Hermes CLI reference
├── scripts/
│   ├── sync-skills.sh         # Pull skills from Hermes to repo
│   ├── sync-memory.sh         # Export memory to markdown
│   └── restore.sh             # Restore from repo to Hermes
└── plans/
    └── 2026-05-24_192600-agent-config-repo.md  # This plan
```

## 3. Step-by-Step

### Phase 1: Clone & Scaffold (read-only prep done, executing next)

- [ ] 1.1 Clone `ai-agent-config-live` to local temp dir
- [ ] 1.2 Create directory structure per above
- [ ] 1.3 Write `README.md` with recovery instructions

### Phase 2: Hermes Config Baseline

- [ ] 2.1 Copy `config.yaml` → `hermes/config.yaml` (redact API keys)
- [ ] 2.2 Copy persona → `hermes/SOUL.md`
- [ ] 2.3 Generate `.env.template` from known env vars

### Phase 3: Skills Full Backup

- [ ] 3.1 Copy ALL skills from `~/.hermes/skills/` to `skills/` (preserving category structure)
- [ ] 3.2 Generate `skills/manifest.md` — categorized index of all 89 skills with descriptions
- [ ] 3.3 Verify no broken symlinks or missing reference files

### Phase 4: Memory Export

- [ ] 4.1 Export current memory entries to `memory/user-profile.md`
- [ ] 4.2 Write `memory/environment.md` — OS, GPU, tools, paths

### Phase 5: Tools Catalog

- [ ] 5.1 Write `tools/catalog.md` — all installed CLIs with versions
- [ ] 5.2 Write `tools/codex.md` — setup steps, flags, usage patterns
- [ ] 5.3 Write `tools/github.md` — auth setup, common commands
- [ ] 5.4 Write `tools/hermes.md` — key commands, config paths

### Phase 6: Automation Scripts

- [ ] 6.1 Write `scripts/sync-skills.sh` — update skills from Hermes to repo
- [ ] 6.2 Write `scripts/sync-memory.sh` — export memory
- [ ] 6.3 Write `scripts/restore.sh` — restore to a fresh Hermes install

### Phase 7: Commit & Push

- [ ] 7.1 Commit all files with descriptive message
- [ ] 7.2 Push to GitHub

## 4. Key Design Decisions

- **Private repo** — skills, memory, and config contain environment specifics that shouldn't be public
- **Redacted config** — `config.yaml` included but with API key values replaced by `$ENV_VAR` references
- **Full skill backup** — all 89 skills stored with complete SKILL.md + references + templates. Disaster recovery: clone → run restore.sh → Hermes is fully operational
- **No binary artifacts** — repo is text-only (markdown, yaml, shell scripts)
- **Idempotent scripts** — sync scripts can run anytime without duplicating data
- **Living backup** — designed for periodic re-sync, not one-shot

## 5. Risks & Open Questions

- **Config drift** — config.yaml will drift from live state. Mitigation: timestamp in header, re-sync script
- **Skill duplication** — bundled skills are versioned upstream and may diverge. Mitigation: sync scripts pull latest on each run; git history tracks changes.
- **Token exposure** — slight risk if redaction misses something. Mitigation: manual review before push

## 6. Validation

- [ ] All markdown files render correctly on GitHub
- [ ] `sync-skills.sh` runs without errors
- [ ] No API keys or tokens in any committed file
- [ ] `README.md` recovery instructions work on a fresh machine
