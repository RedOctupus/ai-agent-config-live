---
name: business-context-first-agent-design
description: Use when designing or modifying Agents, multi-Agent workflows, capability modules, role views, memory behavior, or cross-domain business features, especially when a request starts from a role, page, tool, or Agent name instead of the business context.
---

# Business-Context-First Agent Design

## Core rule

Do not design from a role, page, tool, or Agent name. First identify the business domain, lifecycle stage, role task, context, business result, human boundary, and downstream state change. Only then define Agents, atomic capabilities, capability modules, and role views.

Use this as a design gate for L2/L3 work, not as a reason to model a local bug or copy change.

## Choose the smallest depth

| Level | Trigger | Required work |
|---|---|---|
| L0 | Local bug, copy, non-behavioral UI | Keep scope local; read only affected context. |
| L1 | Change inside an existing scenario or contract | Check the affected lifecycle slice and contract. |
| L2 | New Agent, capability module, role view, memory behavior, or scenario | Run the full gate below. |
| L3 | Coordinator, cross-domain flow, new lifecycle, or platform-wide memory/policy | Full gate plus project flow, handoffs, conflicts, and state return. |

A controlled spike may be YELLOW, but its simulated facts and replacement points must be explicit.

## Kit-aware storage

Read the project's normal entry points first: `AGENTS.md`, `MEMORY.md`, and relevant requirements/flow/framework documents.

If project-memory-kit is present, use `docs/memory/BUSINESS-CONTEXT.md` as the index and write detail to existing slots:

- role tasks and acceptance -> `REQUIREMENTS.md`
- lifecycle and orchestration -> `FLOW.md`
- Agents, atomic capabilities, modules, layers, and contracts -> `FRAMEWORK.md`
- context gaps -> `TODO.md`
- decisions -> `ITERATION.md`
- short snapshot -> `MEMORY.md`

Do not create a parallel memory tree or overwrite existing project documents. Without Kit, use `docs/agent-context/` with `BUSINESS-CONTEXT.md`, `AGENT-DESIGN.md`, and `OPEN-QUESTIONS.md`.

## Full gate for L2/L3

1. **Domain and boundary** - name the owning domain, adjacent domains, upstream input, downstream consumer, and explicit out-of-scope.
2. **Lifecycle** - map the stages/states, locate the requested stage, prerequisites, state transition, downstream work, and uncovered stages.
3. **Role task** - for each relevant role record trigger, task/pain, expected business result, human responsibility, and acceptance condition. Roles are permission and responsibility views, not Agent boundaries.
4. **Context** - label business, objects, time, rules, memory, and evidence as known, simulated, assumed, unknown, or requiring human confirmation. Never hide a gap in a prompt.
5. **Agent boundary** - name each Agent by a stable business result, not a role or one tool. Record inputs, outputs, collaborators, atomic capabilities, memory read/write, human confirmation, failure/conflict handling, and evaluation criterion.
6. **Module and view** - a capability module is a product/business bundle for a lifecycle slice; it may contain one or more Agents and atomic capabilities. Agent-to-module is many-to-many. Map role views last; a view changes permissions, context, framing, and human gates, not business logic.
7. **Orchestration contract** - before Agent-to-Agent implementation, define the collaboration graph: node responsibility, edge trigger, input context, output business result, evidence/confidence, uncertainty, failure/degrade, conflict merge, human gate, state-transition authority, and memory boundary. LangGraph or another framework is an implementation choice, not the contract.
8. **Project return** - for L3, show cross-domain handoffs, result conflicts, human decisions, project-level state changes, and memory updates.

## Decisive Agent/module test

Calling many Agents does not by itself make a module. A component remains a **coordinator Agent** when it owns one composite, independently testable business result in one lifecycle slice and one human decision boundary. Model it as a **capability module** when it bundles multiple independently accepted business results, crosses independent lifecycle transitions, or contains distinct role-specific allocation/review boundaries. A routing/state/retry/tool wrapper with no business result is an orchestrator/service, not an Agent.

## Decision gate

- **GREEN** - domain, lifecycle, role task, context, Agent result, atomic capabilities, memory, human boundary, module, and view are clear; implementation may start.
- **YELLOW** - assumptions or simulated integrations are explicit; implement only the controlled slice.
- **RED** - the request is still only a role, Agent name, page, or tool idea; collect the smallest missing context and stop implementation.

## Response discipline

- For RED: state why implementation is blocked, list only missing decision-changing context, ask at most five unlocking questions, and give the next action.
- For YELLOW: show assumptions, prototype boundary, and smallest slice.
- For GREEN: summarize the domain, lifecycle stage, Agent result, module, view mapping, and implementation plan.
- Do not print a full tool/API plan before the business gate is clear.

## References

Open only when needed:

- `references/lifecycle-analysis.md` - lifecycle and state table.
- `references/context-inventory.md` - context checklist and gap labels.
- `references/agent-boundary.md` - Agent contract and Agent/module decision tests.
- `references/review-gates.md` - GREEN/YELLOW/RED review output.

## Common failures

Agent-first; Role-as-Agent; Tool-as-Agent; UI-first; lifecycle-half (detection without responsibility, remediation, verification, or closure); context-blind design; memory-as-database; no-human-boundary; treating a capability module or graph orchestrator as one Agent.
