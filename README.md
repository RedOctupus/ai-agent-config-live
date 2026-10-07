# AI Agent Configuration - Live Backup

Private backup of my Hermes Agent configuration, skills, memory, and installed tools.

**Machine:** Windows 10 workstation  
**Hermes:** v0.14.0 (DeepSeek v4 Pro)  
**Last sync:** 2026-10-07


## Cursor 个人技能备份规则

仓库：`materials/agent-skills/cursor/`（详见 [`materials/agent-skills/README.md`](materials/agent-skills/README.md)）。

- **只往远程更新**：本机 `~/.cursor/skills` → 本仓库；有变化才提交推送。
- **不自动拉本机、不自动注册**：除非明确说从远端拉某个技能下来用。
- **目录**：目前一个运行时夹里平铺；成套技能放 `cursor/suites/`。以后技能多了可能再分类。
- **含 Superpowers 插件技能备份**：落到 `materials/agent-skills/cursor/plugins/superpowers/`（来自插件缓存，不是 `~/.cursor/skills`）。
- **不含**：Cursor 内置 `skills-cursor`；其他插件默认仍不备份。

## 新增设计模块

本仓新增 `business-context-first-agent-design`，用于在新增或修改 Agent、能力模块、角色视图、多 Agent 协作、记忆行为和跨业务域流程前，先完成：

```text
业务域 → 生命周期 → 角色任务 → 上下文 → Agent 业务结果
→ 原子能力 → 能力模块 → 角色视图 → 跨域回流
```

- portable、Claude、Cursor 三份 Skill 保持同步；
- project-memory-kit 升级到 v1.5.0：BUSINESS-CONTEXT 模板补齐 Agent 协作契约与 Agent↔能力模块多对多边界；
- Kit 项目使用 `BUSINESS-CONTEXT.md` 作为索引和开发前门闸；
- 本仓 `memory/kit/` 已记录该模块的需求、框架、流程、验证和交接信息；
- 详细验证记录见 `memory/kit/annex/VERIFY-20260927-business-context-agent-design.md`。

新增 portable `agent-memory-design` Skill：按业务痛点选择简单状态、Hindsight 局部能力或完整逻辑架构，并提供来源与回答回流规则、模块契约、实施配方、场景验收案例及可选 DeepEval 回归用例。

## Project Memory Kit（仓内 v1.7.1）

权威源为 `materials/agent-skills/{claude,cursor}/project-memory-kit/` 两份一致副本。用户本轮明确授权后，Codex / Claude Code / Cursor 的本机 Kit 已更新；AOCI MCP 已绑定本配置仓，地图尚未初始化。新项目仍分别选择单人/多人、是否启用 AOCI；团队个人地图只作提案，源码先合后维护全局图。

AOCI 官方 Windows AMD64 发布包、许可证与校验值保存在 `materials/tools/aoci/`。拉取本仓后运行 `python scaffold/scripts/install-memory-tools.py install --apply` 即可从本仓安装，项目 MCP 用 `configure --repo <绝对 Git 根> --apply` 注册；仅更新 Kit 可加 `--component kit`。默认预览，显式更新，保留旧版本和备份。详见 [安装与更新](materials/tools/aoci/README.md) 与 [本次部署验收](memory/kit/annex/VERIFY-20261006-memory-tools-deploy.md)。

## Cursor CLI Controller（0.1.0）

新增 [Codex 协调技能](materials/agent-skills/codex/cursor-cli-controller/SKILL.md)：按任务选择 Cursor 原生 subagents/TDD，分配、监控、停止、续接并独立验收。`cursor-controller` MCP 始终保存独立审计；有 Kit 时使用既有 VERIFY/ITERATION 作为带责任署名的项目记录，不修改 Kit 本体。

使用前置、MCP/Kit 检测、版本来源、显式安装与配置命令见 [介绍与接入](materials/tools/cursor-controller/README.md)。原始环境、密钥和审计日志不入库；源码在 `materials/agent-skills/codex/`，依赖仅安装到技能私有环境。仓库拉取不自动安装/注册。

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
    ├── cursor-user-rules/    ← Cursor 账号 User Rules 快照（借鉴用，不注入本仓）
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
