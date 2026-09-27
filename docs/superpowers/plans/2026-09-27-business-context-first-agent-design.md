# 业务上下文优先 Agent 设计 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Add a reusable business-context-first Agent design skill and integrate it with project-memory-kit without creating a parallel memory system.

**Architecture:** Keep the design method in a portable skill with focused references. Add one optional `BUSINESS-CONTEXT.md` template and routing instructions to the two project-memory-kit copies. Synchronize the skill into portable, Claude, and Cursor backup trees, then validate with artifact checks and a repeatable DeepSeek-backed sandbox pressure suite.

**Tech Stack:** Markdown skill documents, Python standard library validation scripts, existing Git/PowerShell workflow; no new runtime dependency.

**Spec:** `docs/superpowers/specs/2026-09-27-business-context-first-agent-design.md`

## Global Constraints

- Do not touch secrets or install local skills automatically.
- Do not add runtime dependencies.
- Keep Claude and Cursor project-memory-kit copies byte-equivalent.
- Keep portable, Claude, and Cursor copies of the new design skill byte-equivalent.
- Preserve existing project-memory-kit structure and version the kit because a new template and routing behavior are added.
- Keep sandbox outputs under ignored `materials/_local/`.

---

### Task 1: Add the failing/pressure test harness before the skill

**Files:**
- Create: `materials/_local/business-context-skill-sandbox/scenarios.json`
- Create: `materials/_local/business-context-skill-sandbox/run_baseline.py`
- Create: `materials/_local/business-context-skill-sandbox/score_baseline.py`

- [x] Run the six baseline prompts without the new guidance.
- [x] Record outputs and score missing domain/lifecycle/role/context/agent/view/human-gate/unknown handling.
- [x] Preserve raw outputs only under ignored `materials/_local/`; summarize findings in the verification record, not in the permanent skill.

Expected baseline: role/agent/UI-first prompts jump to implementation and do not consistently establish the business domain, lifecycle, or task context; the explicit small-fix prompt remains scoped.

---

### Task 2: Create the portable design skill and references

**Files:**
- Create: `materials/agent-skills/portable/business-context-first-agent-design/SKILL.md`
- Create: `materials/agent-skills/portable/business-context-first-agent-design/references/lifecycle-analysis.md`
- Create: `materials/agent-skills/portable/business-context-first-agent-design/references/context-inventory.md`
- Create: `materials/agent-skills/portable/business-context-first-agent-design/references/agent-boundary.md`
- Create: `materials/agent-skills/portable/business-context-first-agent-design/references/review-gates.md`

**Interfaces:**
- Consumes: user task, project entry files, optional `docs/memory/BUSINESS-CONTEXT.md`, and existing project documents.
- Produces: task level, domain/lifecycle/context checklist, agent/capability boundary, GREEN/YELLOW/RED decision, and documented next action.

- [x] Write the frontmatter with `Use when...` triggers and no process summary in the description.
- [x] Write the core L0–L3 routing and kit-aware/standalone behavior in `SKILL.md`.
- [x] Write lifecycle, context, agent-boundary, and review-gate details in references so the entrypoint stays scannable.
- [x] Include explicit anti-patterns: Role-as-Agent, Tool-as-Agent, UI-first, Agent-first, lifecycle-half, context-blind, memory-as-database, and no-human-boundary.
- [x] Include one construction-neutral example and one compact task table; avoid making CMP-specific schema mandatory.

---

### Task 3: Add the project-memory-kit shared template and routing

**Files:**
- Create: `materials/agent-skills/claude/project-memory-kit/templates/BUSINESS-CONTEXT.md`
- Create: `materials/agent-skills/cursor/project-memory-kit/templates/BUSINESS-CONTEXT.md`
- Modify: `materials/agent-skills/claude/project-memory-kit/SKILL.md`
- Modify: `materials/agent-skills/cursor/project-memory-kit/SKILL.md`
- Modify: `materials/agent-skills/claude/project-memory-kit/templates/AGENTS.md`
- Modify: `materials/agent-skills/cursor/project-memory-kit/templates/cursor-rule.mdc`

- [x] Add `BUSINESS-CONTEXT.md` to the documented init layout as an optional L2/L3 Agent-design slot.
- [x] Add routing: Agent/capability/module/view/multi-agent/memory/cross-domain changes load `business-context-first-agent-design`.
- [x] Add mapping rules to REQUIREMENTS/FLOW/FRAMEWORK/TODO/ITERATION without copying all design content into MEMORY.
- [x] Add kit-aware behavior: use `docs/memory/BUSINESS-CONTEXT.md`; do not create parallel `agent-design/` trees.
- [x] Update kit version from `1.3.1` to `1.4.0` because a new optional template and new routing behavior are introduced.
- [x] Keep Claude and Cursor copies byte-equivalent after edits.

---

### Task 4: Add standalone compatibility guidance and manifest entries

**Files:**
- Modify: `materials/agent-skills/portable/business-context-first-agent-design/SKILL.md`
- Modify: `materials/agent-skills/claude/project-memory-kit/README.md`
- Modify: `materials/agent-skills/cursor/project-memory-kit/README.md`
- Modify: `materials/agent-skills/README.md`

- [x] Document standalone fallback under `docs/agent-context/` with `BUSINESS-CONTEXT.md`, `AGENT-DESIGN.md`, and `OPEN-QUESTIONS.md`.
- [x] State that existing project docs are reused and never overwritten.
- [x] Add the skill to the repository skill inventory.
- [x] Avoid claiming local installation or automatic registration.

---

### Task 5: Build repeatable validation and run the green suite

**Files:**
- Create: `materials/_local/business-context-skill-sandbox/run_guided.py`
- Create: `materials/_local/business-context-skill-sandbox/score_guided.py`
- Create: `materials/_local/business-context-skill-sandbox/test_artifacts.py`
- Create: `memory/kit/annex/VERIFY-20260927-business-context-agent-design.md`
- Modify: `memory/kit/ITERATION.md`
- Modify: `memory/kit/HANDOVER.md` if the repo handover fact changes

- [x] Run artifact checks: frontmatter, required headings, template references, copy equality, and kit version consistency.
- [x] Run the six scenarios with the new Skill guidance prepended; save raw outputs under ignored `_local`.
- [x] Score that L2/L3 scenarios explicitly establish domain/lifecycle/context before implementation and that the L0 small fix stays scoped.
- [x] Inspect all outputs for prompt verbosity, repeated instructions, and loopholes; shorten the Skill where possible without weakening gates.
- [x] Run `python scaffold/scripts/check-memory-size.py`.
- [x] Record tests, baseline, guided results, and residual risks in the VERIFY file.

---

### Task 6: Final repository review

**Files:**
- Review all changed files; no new source file expected.

- [x] Run `git diff --check`.
- [x] Run `git status --short` and confirm no secrets or ignored sandbox output are staged.
- [x] Confirm Claude/Cursor kit copies are identical.
- [x] Confirm portable/Claude/Cursor design skill copies are identical.
- [x] Summarize the final integration behavior and whether DeepEval was needed.
