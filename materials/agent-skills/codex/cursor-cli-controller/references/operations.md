# Runtime and MCP operations

Read this to set up the local server, submit a contract, monitor a task or recover a failed/stale run. Both MCP and CLI use the same independent task/audit store. Defaults are under the user's local application data directory (`CursorController` on Windows).

## Calling tools

The Codex host registers `cursor-controller`. Its tools are `cursor_doctor`, `cursor_capabilities`, `cursor_submit`, `cursor_status`, `cursor_watch`, `cursor_stop`, `cursor_resume`, `cursor_result`, `cursor_verify`, `cursor_record_acceptance`, `cursor_audit`, and `cursor_list_tasks`.

MCP responses use `{ "ok": true, "data": ... }` or `{ "ok": false, "error": { "code": ..., "message": ..., "details": ... } }`. An execution/verification failure may be valid returned data, so inspect the actual state/exit fields. A successful tool invocation does not establish task acceptance. `cursor_doctor.data.data_dir` identifies the actual audit location; when using an external CLI, pass that same `--data-dir` because app and terminal environment profiles can have different defaults.

Status/watch take a task ID and an event cursor. Reuse the returned cursor, and inspect `run_id` after resume. Wait up to 30 seconds at a time, then continue the coordinating conversation and issue another bounded call if required. A quiet model call is not a failure or a reason to create a duplicate task.

Do not use `agent ls` as an assumed JSON process-status API. Session history and a process running status are different. The controller's persisted run and actual event/exit records are the tracking source.

## Local setup and CLI fallback

Resolve the actual folder containing this SKILL.md. The installed Windows example is:

```powershell
$skillDir = Join-Path $env:USERPROFILE '.codex\skills\cursor-cli-controller'
$pythonExe = Join-Path $skillDir '.venv\Scripts\python.exe'
$controllerCli = Join-Path $skillDir 'scripts\cursor_control.py'
& $pythonExe $controllerCli --help
```

Use the actual installed path on other machines. If the private environment is missing, create it with a Python 3.10+ interpreter and install `requirements.txt`; do not modify a shared Python environment. Core CLI operations require only the standard library; the server requires the pinned MCP SDK.

The actual installed MCP launch command is the private Python executable plus `scripts/mcp_server.py`. The Codex CLI supports registering a stdio launch command with:

```powershell
$serverScript = Join-Path $skillDir 'scripts\mcp_server.py'
codex mcp add cursor-controller -- $pythonExe $serverScript
```

Inspect existing configuration first, preserve other entries and back up the file before updating. Do not overwrite another server with that name without resolving its relevance. This task MCP is registered only with Codex. Cursor retains its own existing tools/configuration. Hosts may need to reload after registration; use the CLI fallback while this conversation lacks the newly registered tools.

Run CLI `--help` for the actual flags. Submit receives a UTF-8 contract file, acceptance receives a JSON receipt file, and every continuation references the recorded task ID. Point CLI and MCP at the same `--data-dir` when overriding the default.

## Task contract

Resolve paths and available skill bindings before submission. This minimal shape illustrates a writable TDD task with independent command verification:

```json
{
  "workspace": "C:/work/example-project",
  "objective": "Fix the CSV export boundary case and preserve existing behavior.",
  "acceptance": ["The reproduced boundary case passes", "Existing export tests pass"],
  "coordinator": {
    "id": "codex:current-conversation", "kind": "agent", "host": "codex",
    "role": "coordinator", "source": "declared"
  },
  "strategy": ["tdd"],
  "allow_writes": true,
  "timeout_seconds": 3600,
  "verification_commands": [["python", "-m", "unittest", "discover", "-s", "tests", "-v"]],
  "verification_timeout_seconds": 300,
  "evidence_paths": ["export.py", "tests/test_export.py"],
  "write_ownership": {"cursor-cli": ["export.py", "tests"], "codex": []},
  "memory": {"required": false},
  "aoci": {"required": false}
}
```

Replace the example project, commands, evidence paths and identity with actual task data. Do not retain model choices from an example. `skill_bindings` can assign required available instructions to their real host and path; omit unused capabilities. With `allow_writes: false`, use the CLI's supported read-only mode. A prompt alone does not enforce filesystem permissions.

For an explicitly assigned directory whose contents are trusted for this task, set `trust_workspace: true` when headless read-only execution otherwise needs a workspace trust prompt. The runtime passes `--trust` separately from write permissions. This does not change ask mode into agent mode or enable `--force`. Keep this choice in the task contract rather than globally changing Cursor permissions.

The runtime passes a short fixed role prompt referring to a task contract file. The contract supplies objective, acceptance, selected workflows, ownership and evidence instructions. This preserves Chinese text, multiline prompts and shell metacharacters without executing the task text as shell code.

`cursor_capabilities` also returns `project_memory`. It checks known entry locations (`docs/memory`, this source repo's `memory/kit`, or workspace root), without recursive collection. `present=false` means no entry found; unreadable/unsafe entries have a diagnostic and unknown presence. `memory_schema_version` comes from the explicit initialization line, not an incidental progress version. AOCI states distinguish `enabled`, `disabled`, `configured_not_initialized` and `unknown`; a configured but uninitialized map does not require pretending AOCI delivery is complete.

On Windows, if the calling MCP process is inside a host Job Object, the worker is launched through a current-user, least-privilege, one-shot Task Scheduler broker. A hidden pythonw bootstrap records the real worker PID and removes only its validated launch entry. Ordinary uncontained CLI calls can use detached process launch. This uses the built-in scheduler with no recurring trigger or persistent system service. An unavailable or uncertain broker returns a diagnostic and retains conservative ownership; it does not pretend the task safely started or stopped.

## Verification and acceptance

After execution is quiescent, Codex inspects the result and prepares any required Kit/AOCI updates. Use preliminary tests if necessary to decide the technical result, then finish the registered memory-file changes before obtaining final closure evidence. Do not freeze file hashes and subsequently edit those same files during writeback.

`cursor_verify(task_id, run_id)` executes only commands registered in the contract, without shell-string composition. It returns actual command exits/logs and artifact hash evidence. Codex still checks whether those tests and artifacts address the acceptance criteria. Record the final decision while those files remain unchanged. A decided run is immutable; resume before obtaining evidence for a new decision.

Send current-run evidence returned by verify to `cursor_record_acceptance`. Supply executor, author, reviewer and decision maker attribution plus the decision and authorization bases. Keep declared identities declared; do not claim the current user reviewed a patch unless there is an actual decision reference.

Memory receipts use the exact task/run, completion state, explicit `performed_by` Actor and current project file evidence. AOCI receipts similarly reference the current run, registered host, explicit actual performer and checked outputs from the configured service. Report authorship is separate from who performed maintenance. Required maintenance cannot be replaced by a bare statement that everything is done. The [responsibility contract](calling-and-memory.md) specifies host selection and report fields.

Machine receipt shape:

```text
memory: task_id, run_id, state="completed", performed_by=<actual Actor>, evidence=<current project artifact receipts>
aoci:   task_id, run_id, state="checked", host=<configured host>, performed_by=<actual Actor>, evidence=<current project artifact receipts>
```

If required Kit paths have different owners, use a grouped memory receipt:

```text
task_id, run_id, state="completed", actions=[
  {performed_by=<Codex project-memory Actor>, evidence=<current project-memory artifacts>},
  {performed_by=<Cursor module-memory Actor>, evidence=<current module-memory artifacts>}
]
```

Use exact returned verification artifacts rather than new evidence descriptions. All pending paths must be covered once, and each action must match that path's declared owner. Stored actions contain their own receipt IDs and `recorded_by`; the aggregate memory receipt links them. A report author can record several maintenance performers without becoming their executor.

Set `memory.mode` to `coordinator` or `executor`, or bind an explicit maintenance `host`, when assigning responsibility. Use actual pending memory paths in `memory.pending_paths`; they must already exist. Their hashes are part of final verification. Match maintenance performer to the resolved path owner and configured AOCI host.

Prepare project records using actual execution/review facts and a task/run reference. The final MCP-rendered report carries the actual decision receipt. Use a fresh authorized VERIFY path for that report; don't rewrite an existing hashed execution report after closure. If a subsequent project edit changes registered evidence, treat it as a new writeback/verification cycle instead of silently modifying the finalized receipt.

A managed report path may be in the task storage or an explicitly authorized project report location. Existing report content must be preserved or revision checked; do not overwrite someone else's VERIFY file. With Kit, references to audit receipts go into existing VERIFY/ITERATION slots. Without Kit, reports remain in managed storage.

## Failure and recovery

- CLI missing or authentication absent: return the diagnostic and resolve that specific dependency. Do not expose credentials or launch a login browser without a setup reason.
- Nonzero exit, truncated stream or no valid terminal result: execution is failed/incomplete even if the assistant says done. Keep stdout/stderr and report the actual cause.
- Stop/timeout: request task-scoped process-tree termination, then wait for confirmed quiescence. Unconfirmed descendants keep the workspace occupied; do not begin shared-file writeback.
- Broken MCP stdio: restart the connection and query the same data directory. Worker lifetime is independent of that connection.
- Worker/process identity unknown after interruption: inspect actual process/audit evidence, preserve uncertain state and avoid a second overlapping writer. OS restart does not guarantee task survival.
- New instruction after an accepted run: resume the exact Cursor session as a new run, with fresh verification, approval and required maintenance receipts. Historical receipts do not approve new artifacts.
- External edits or stale hashes: obtain current evidence and reconcile changes; do not force old results into current project memory.
- Required skill/service unavailable on its assigned host: report the actual missing capability. Choose a supported strategy only when it still meets the task; record that adjustment.

The audit store provides local evidence and append-only API history. It does not prevent an external program from bypassing the controller and editing files, and attribution fields do not authenticate human identities.
