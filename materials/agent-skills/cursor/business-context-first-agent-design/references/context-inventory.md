# Context inventory

Use this as a compact preflight instead of inventing missing context.

| Context class | Questions | Status labels |
|---|---|---|
| Business | project, phase, area, work package, activity, current state? | known / simulated / unknown |
| Objects | event, document, contract, person, equipment, task, evidence? | known / simulated / unknown |
| Time | effective period, deadline, version, prior handling? | known / assumed / unknown |
| Rules | policy, regulation, permissions, human-only decision? | known / pending confirmation |
| Memory | prior case, decision, preference, unresolved fact, conflict? | read / write / not applicable |
| Evidence | source, timestamp, confidence, completeness, external use? | sufficient / incomplete / unavailable |

## Gap rule

Never hide a gap inside a prompt. Put it in the project context index, mark whether it blocks implementation, and choose one action: ask, simulate, defer, or stop.
