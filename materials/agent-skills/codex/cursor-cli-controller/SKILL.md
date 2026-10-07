---
name: cursor-cli-controller
description: Use when Codex needs to delegate coding or exploration to Cursor Agent CLI, monitor a Cursor task across turns, resume or stop it, verify its results, or trace who executed and approved its delivery. Applies to projects with or without MEMORY kit.
metadata:
  skill-version: "0.1.0"
---

# Cursor CLI Controller

Codex owns the user-facing goal, dispatch and final acceptance. Cursor executes within the assigned scope and selects its local tools. The task MCP owns independent machine audit; project MEMORY is optional.

## Identify the calling role

If the current task contract says `role: executor` or this session was delegated by this controller, execute that contract with Cursor's native tools. Report evidence and memory changes to the coordinator. Do not start another controller task or invoke its MCP control tools.

For the coordinating Codex session, use this workflow:

1. Read project entry rules and relevant existing changes. Determine objective, writable paths and observable acceptance criteria. If Kit exists, read its MEMORY entry and applicable ownership rules.
2. Check `cursor_doctor` and `cursor_capabilities` for the target workspace. Read the returned `project_memory` entrypoint, schema version and explicit AOCI state; absence is normal, unknown requires inspection. Bind each needed skill/tool to its decision owner, execution host, write owner and evidence owner. A readable skill file is not proof it was invoked. See [calling-and-memory.md](references/calling-and-memory.md).
3. Choose Cursor's strategy by the actual task: native subagents for independent exploration; TDD for testable behavior; reproduce and diagnose unexplained failures; plan before large uncertain changes; direct execution and suitable verification for small edits. Strategies can be combined. Preserve user-selected models and project conventions.
4. Submit a UTF-8 task contract through `cursor_submit`. Use the returned task/run IDs for all monitoring and decisions. `cursor_watch` returns bounded new events and a cursor. Inspect and explain meaningful changes; do not restart quiet or still-running tasks.
5. After all managed writers stop, inspect artifacts against acceptance criteria. Codex reviews memory proposals and completes required Kit/AOCI writeback, recording who performed each maintenance action. If preliminary tests inform that review, their result is not yet the final closure evidence.
6. Once all registered code, evidence and required memory files are stable, run `cursor_verify` for the contract's registered commands. Record acceptance using those fresh hashes, explicit attribution and maintenance receipts. File edits after verification require fresh verification; a finalized run needs resume before a new decision. Produce the signed responsibility report without inferring a human's approval from an agent's result.

MCP audit is recorded for every project. Without Kit, keep reports in managed task storage; do not initialize Kit. With Kit, use existing VERIFY/ITERATION slots and reference the same task/run/audit receipts. Keep raw logs out of MEMORY snapshots.

## Responsibility record

Every execution report and iteration identifies **executor, report author, reviewer, decision maker, decision status, time, basis and receipt IDs**. Missing review/decision is `pending`, with no invented approver. Runtime-observed actions and caller-declared names remain distinguishable. These are attribution records, not cryptographic signatures.

Project-level state defaults to Codex; Cursor writes execution facts and assigned module memory. Follow an existing project's executor-owned mode when explicitly applicable, with a single writer and handoff. Read the exact signature and writeback contract in [calling-and-memory.md](references/calling-and-memory.md).

## Operations

Use the installed `cursor-controller` MCP tools when available. When the host has not reloaded MCP, use the same core's CLI rather than start a second state store. See [operations.md](references/operations.md) for setup, contract fields, command examples, evidence receipts and failure recovery.

Do not add force permission for read-only tasks, approve all MCP servers, modify global Cursor permissions, or substitute GUI automation for this CLI workflow. Permission to implement a task covers its required local work; external publication or messaging requires the applicable user authorization.
