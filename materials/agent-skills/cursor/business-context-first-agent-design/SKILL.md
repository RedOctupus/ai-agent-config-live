---
name: business-context-first-agent-design
description: Use when designing or modifying agents, multi-agent workflows, capability modules, role views, memory behavior, or domain-driven features, especially when a request risks jumping directly to a role-named agent, a single tool, or a UI without establishing the business domain, lifecycle, role task, context, boundaries, and cross-domain effects.
---

# Business-Context-First Agent Design

## Core principle

Do not design an Agent from its name, role, page, or first tool request. Start from the business domain and its lifecycle, identify the role task and required context, then define Agent responsibilities, atomic capabilities, capability modules, and role views. Return to the project-level business flow before implementation so the task's upstream and downstream effects are visible.

Use this skill as a design gate, not as a reason to over-model small fixes.

## Routing: choose the smallest sufficient depth

Classify the request before proposing code:

| Level | Typical request | Required behavior |
|---|---|---|
| L0 | A local bug, copy change, or non-behavioral UI fix | Keep scope local. Read existing context; do not create a new domain model. |
| L1 | An extension inside an existing scenario or Agent contract | Read the relevant domain/lifecycle slice and update only affected contracts. |
| L2 | A new Agent, capability module, role view, memory read/write, or new business scenario | Run the full business-context gate before implementation. |
| L3 | Cross-domain orchestration, a coordinator, a new lifecycle, or platform-wide memory/policy change | Run the full gate plus project-level flow, cross-domain handoffs, conflict handling, and human decision boundaries. |

If the user explicitly says this is a throwaway spike, keep the analysis lightweight but label assumptions and simulated context.

## Storage and Kit integration

1. Read the project's normal entry points first: `AGENTS.md`, `MEMORY.md`, and any existing requirements/architecture/workflow/agent documents.
2. If project-memory-kit is present, use `docs/memory/BUSINESS-CONTEXT.md` as the index and write details to the existing Kit slots:
   - role tasks and acceptance → `REQUIREMENTS.md`
   - domain lifecycles and orchestration → `FLOW.md`
   - Agents, atomic capabilities, capability modules, and layers → `FRAMEWORK.md`
   - actionable context gaps → `TODO.md`
   - decisions and reasons → `ITERATION.md`
   - short current snapshot → `MEMORY.md`
3. If project-memory-kit is absent and the task is L2/L3, use a minimal compatibility store under `docs/agent-context/`:
   - `BUSINESS-CONTEXT.md`
   - `AGENT-DESIGN.md`
   - `OPEN-QUESTIONS.md`
4. Never overwrite existing project documentation. Reuse existing conventions and add pointers. Do not create a second parallel memory system when Kit already exists.
5. If the relevant context store is missing, say what you will initialize before creating it.

## Required analysis for L2/L3

Complete these in order. Do not start implementation until the gate is GREEN or the user explicitly accepts a YELLOW controlled prototype.

### 1. Locate the business domain

State:

- Which business domain owns the task;
- Whether adjacent domains are involved;
- The upstream input and downstream consumer;
- The domain boundary and what is explicitly out of scope.

### 2. Map the domain lifecycle

Write the lifecycle as states or stages, for example:

```text
发现 → 判断 → 分派 → 执行 → 复核 → 关闭 / 升级 / 复发
```

Locate the requested task in that lifecycle and state:

- prerequisites;
- state transition produced by the task;
- downstream work unlocked by the result;
- lifecycle stages intentionally not covered.

### 3. Identify role tasks and scenarios

For every relevant role, state:

- trigger;
- task and pain point;
- desired business result;
- human decision or responsibility;
- success/acceptance condition.

Roles are users, responsibility holders, permission boundaries, and views. They are not automatically Agent boundaries.

### 4. Inventory context

Separate the context into:

- business: project, phase, area, work package, activity, current state;
- objects: events, documents, contracts, people, equipment, tasks, evidence;
- time: effective period, deadlines, versions, prior handling;
- rules: policy, regulation, permissions, non-negotiable human gates;
- memory: prior cases, decisions, preferences, unresolved facts, conflicts;
- evidence: sources, timestamps, confidence, completeness, external-output eligibility.

Label each item `known`, `simulated`, `unknown`, `assumed`, or `requires human confirmation`. Do not silently fill a gap with a plausible value.

### 5. Define Agent responsibilities

Name Agents by a stable business responsibility or result, such as `weekly-report-agent`, `handover-agent`, or `risk-triage-agent`.

For each Agent define:

- business result owned;
- inputs and outputs;
- collaborating Agents;
- atomic capabilities it may call;
- memory it may read and write;
- permissions and human confirmation points;
- failure, conflict, and escalation behavior.

Avoid:

- `supervisor-agent` or `safety-manager-agent` when the name only describes a role;
- `query-agent` or `format-agent` when the unit is only a tool action;
- an Agent with no distinct result or evaluation criterion.

### 6. Define atomic capabilities and capability modules

Atomic capabilities should be reusable and independently testable: query, retrieve memory, compare versions, aggregate, classify, generate a draft, check evidence, create a task, request confirmation, or write memory.

A capability module packages a business result and lifecycle slice, including:

- covered domain and lifecycle stages;
- supporting Agents;
- atomic capabilities;
- shared context;
- memory policy;
- human boundaries;
- inputs, outputs, and state transitions;
- consuming role views.

### 7. Map role views last

Only after the capability module is clear, map it to role views:

- what each role can see;
- which result is prioritized;
- which Agent calls are available;
- which actions are allowed;
- which actions require confirmation;
- what is read-only or simulated.

A role view is a projection of shared capabilities, not a separate copy of the business logic.

### 8. Return to the project flow

For L3 or cross-domain work, check:

- which domain modules are called;
- how shared context is passed;
- how Agent results are merged and conflicts surfaced;
- how human decisions feed back into the lifecycle;
- how the project-level state changes;
- what memory is updated after completion.

## Decision gate

Report one of these outcomes:

- **GREEN** — domain, lifecycle, role task, context, Agent result, atomic capabilities, memory, human gates, and view mapping are sufficiently clear; implementation may start.
- **YELLOW** — some context is simulated, assumed, or unavailable, but the limits and replacement points are explicit; implement only a controlled prototype.
- **RED** — the request is still only a role label, Agent name, page, or tool idea; stop and collect the missing business context.

For RED, ask only the smallest questions that unlock the next step. For YELLOW, list the assumptions before coding. For GREEN, keep the implementation plan scoped to the analyzed scenario.

## Response discipline

Keep the first response proportional to the task:

- **RED:** state the level and why implementation is blocked, list only the missing context that changes the decision, ask at most five unlocking questions, and give the next action. Do not print a full Agent/tool/API implementation plan.
- **YELLOW:** show a short assumptions/simulated-context table, the controlled prototype boundary, and the smallest next slice. Do not present simulated facts as settled business rules.
- **GREEN:** summarize the confirmed domain, lifecycle stage, Agent responsibilities, capability module, and view mapping, then move to the implementation plan.
- **L0:** do not demand a new domain model or ask unrelated domain questions. Limit checks to the affected code path, existing contract, and regression boundary.
- Do not quote this Skill or repeat every checklist category when a compact table or pointer is sufficient.

## Quick self-check

Before writing code for an L2/L3 request, answer yes/no:

- [ ] Business domain is named and bounded.
- [ ] Lifecycle and current stage are mapped.
- [ ] Role task and business result are explicit.
- [ ] Required context is listed and labeled.
- [ ] Agent names describe results, not roles or single tools.
- [ ] Agent inputs, outputs, memory, and human boundaries are explicit.
- [ ] Atomic capabilities are separated from Agents.
- [ ] Capability module and lifecycle coverage are explicit.
- [ ] Role views are mapped after the capability design.
- [ ] Cross-domain effects and state return are checked when relevant.
- [ ] Unknowns are not silently invented.

## Common failure modes

- Agent-first: accepting “add an Agent” as a sufficient design.
- Role-as-Agent: creating one Agent per persona.
- Tool-as-Agent: promoting a query or formatter into an Agent without a business result.
- UI-first: defining a button before its lifecycle and decision outcome.
- Lifecycle-half: implementing detection without responsibility, remediation, verification, or closure.
- Context-blind: using only the latest user message and ignoring project, time, permissions, history, and evidence.
- Memory-as-database: storing every observation as durable memory without scope, confidence, validity, or conflict handling.
- No-human-boundary: letting an Agent silently approve, stop work, close a risk, or publish a formal result.
