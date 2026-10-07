# Calling host, memory ownership and attribution

Read this when preparing a contract, sharing a MEMORY kit project, or recording reports and decisions. The controller is a coordinator workflow; it is not a substitute for Cursor's native development capabilities.

## Who calls what

| Capability | Decision owner | Execution host | Result authority |
| --- | --- | --- | --- |
| User clarification, scope, architecture choices and dispatch | Codex | Codex and its relevant skills | User decisions plus declared delegation basis |
| Start/status/watch/stop/resume | Codex | Codex calls controller MCP, which manages CLI | Actual worker/process events |
| Exploration and native subagent assignment | Codex chooses task strategy; Cursor chooses local breakdown | Cursor's actual Task/Explore tools | Cursor returns evidence; Codex assesses conclusions |
| TDD, root-cause investigation, implementation, executor self-tests | Codex specifies constraints; Cursor chooses concrete steps | Cursor's local skills and tools | Actual test/tool output, not an unsupported completion claim |
| Independent verification and final technical acceptance | Codex | Registered verification commands plus Codex inspection | Current-run verification/decision receipts |
| Project-level Kit state | Codex within existing owner authorization | Codex loads the existing Kit | Approved project decisions and verified final status |
| Task facts and assigned existing module memory | Cursor within declared paths | Cursor loads the same installed Kit | Execution facts, self-tests, pending acceptance |
| Existing AOCI source map maintenance | Coordinator resolves the actual configured host | Cursor when available for its workspace, otherwise Codex after handoff | Current service/Guide-required receipts |

Resolve capabilities for each host. Shared skill directories let both agents read the same instructions but do not grant both write ownership. Codex-only app tools cannot be invoked by naming them in a Cursor prompt. Required unavailable capability returns a clear gap; optional capability may degrade with explanation. Do not silently install another service or copy a skill version.

One main Cursor run owns a workspace while executing. Use native subagents for independent work with explicit context, outputs and file boundaries. For parallel editing, establish isolated copies or non-overlapping ownership before allowing writes. Delegated workers do not invoke the controller recursively.

## MEMORY kit

The target project's `docs/memory/` is project memory. The installed `project-memory-kit` skill is the reusable instruction package. This controller does not modify that package, upgrade its version or enable AOCI.

Before dispatch, Codex reads the project's entry rules, MEMORY reading/maintenance table and existing human owners. It records confirmed goals and assigns memory paths. During execution Codex reads the target workspace rather than edit shared files.

The default mode is **coordinator-owned project state**:

- Codex writes project-level MEMORY/root indexes, GLOBAL, project requirements/framework/flow, final TODO status, HANDOVER/REFERENCES and project ITERATION as actually affected.
- Cursor writes assigned code/tests, existing module-local memory and its task-specific VERIFY execution section. It submits `memory_delta` suggestions with source/evidence for project-level changes.
- After the managed process tree is quiescent, Codex validates proposals and completes project-level writeback. Final verification hashes the stable code and memory artifacts; acceptance references that evidence. A fresh signed coordinator VERIFY can record the resulting decision receipt without overwriting an earlier hashed executor report.

Do not create module memory just to divide this task. If the project explicitly requires the executor to write all relevant Kit files, select **executor-owned memory** before dispatch. Cursor is then the sole writer of the specified files during execution. Codex receives write ownership after confirmed stop/handoff. A task contract must not simultaneously require direct Kit writeback and forbid every required memory path.

Version-check affected files at handoff; old proposals cannot overwrite changed facts. An unresolved writer, changed baseline or missing owner authorization prevents writeback until resolved. Do not change the project's human ownership table merely because one agent coordinates this task.

If Kit is absent, use independent task audit/reports only. Mentioning Kit as an example does not authorize initializing it. If Kit exists, keep its normal slots: VERIFY for delivery, ITERATION for meaningful changes, HANDOVER/REFERENCES for their existing purposes. MEMORY contains concise snapshot/pointers, not raw event logs.

An already-enabled AOCI must keep its status when temporarily unavailable. Bind maintenance to the host configured for this exact workspace, follow its current rules/overview/Guide, and record required maintain/verify/check outcomes. Missing maintenance is pending, not a closed delivery. Do not guess AOCI versions, replay receipts from another worktree, or enable/install/update it as a workaround.

## Independent audit and optional Kit projections

The MCP runtime always maintains its own task, run, verification and decision events. Projects without Kit remain fully traceable. Kit reports are curated project documents that cite those events; they do not replace the runtime audit or independently decide that a task succeeded.

Link both using task ID, run ID, contract revision, receipt IDs and evidence file hashes. Audit distinguishes action occurrence from observation/recording time. Caller-provided identities are declared; runtime-observed CLI sessions, process identities and command exits are observed. Local attribution and integrity hashes do not authenticate a human or provide a cryptographic signature.

Each memory/AOCI completion receipt declares `performed_by` for the actual maintenance actor and its host. Audit uses this performer for the maintenance event and retains who recorded/reported it separately. Codex authoring a report must not turn a Cursor-performed source-map update into a Codex-performed action. Performer's identity remains declared unless the runtime itself observed the action.

For required files maintained by both hosts, a memory completion receipt uses `actions`: each action has its own `performed_by` and current artifact `evidence`. Their combined paths cover all required pending paths. Each action receives a separate performer audit receipt; the aggregate uses a runtime service record and links those receipts. A legacy single-performer receipt remains valid. Explicit path ownership takes precedence over the default coordinator/executor mode; an explicit single maintenance `host` still limits the whole receipt. Do not merge two performers into the report author's signature or claim the same evidence twice.

Each resume starts a new run. Old decisions, test receipts and memory/AOCI receipts remain historical and cannot approve the new run. Review the current artifacts, obtain fresh verification, and record current-run maintenance again when required.

## Signature fields for every war report

Use these fields in a task report or VERIFY. Preserve an existing template's structure; add a compact responsibility block rather than rewrite the whole document.

| Field | Required content |
| --- | --- |
| `task_id`, `run_id`, `contract_revision` | Exact runtime identifiers |
| `executed_by` | Actual executor and Cursor session; source of attribution |
| `authored_by` | Who assembled this report |
| `reviewed_by` | Actual reviewer, or pending |
| `decided_by` | Who made this particular decision, or pending |
| `decision_status` | Pending, approved or rejected; execution status is separate |
| `decision_basis` | Criteria and actual evidence/verification receipt IDs |
| `authorization_basis` | User instruction/delegation reference; never invented human approval |
| `recorded_at`, review/decision times | Actual event times; absent decisions have no invented timestamp |
| `audit_receipts` | References to independent runtime audit events |
| `memory_status`, `aoci_status` | Required completed/pending/not-applicable outcomes and evidence |

Actor shape: `id`, `kind` (`agent`, `user`, `service`), `host`, `role`, `source` (`declared`, `observed`). An executor not yet observed has an explicit unknown identity/source rather than a fabricated process ID. Roles are task responsibilities, not newly invented human owners. Separate executor, author, reviewer and decider even when one actor fulfills several roles. Say Codex approved technical acceptance when that is what happened; say the user approved only when actual user decision evidence exists.

Every ITERATION entry preserves the project's existing columns and adds inline executor/author/reviewer/decider information or a direct link to a VERIFY responsibility block carrying all fields. A pending/rejected entry is valid; it must not silently invent a completed review. Updates to earlier facts stay traceable to the new run and evidence instead of erasing prior decisions.

For an executor report before review, a valid compact form is:

```text
task/run: <actual task_id>/<actual run_id>
executed_by: Cursor/<actual session_id> (observed)
authored_by: Cursor (declared)
reviewed_by: pending
decided_by: pending
decision_status: pending
basis: executor test/output evidence; independent verification pending
audit: <actual event/receipt references>
```

Replace brackets with actual returned identifiers. Do not cite nonexistent receipt IDs, turn model self-tests into independent verification, or fill pending signatures with the name of whoever usually approves tasks.
