# Agent boundary

## Agent contract

```text
Name:
Business result owned:
Lifecycle stage / state transition:
Inputs:
Outputs:
Collaborators (Agents):
Atomic capabilities:
Memory read / write:
Human confirmation:
Failure / conflict handling:
Evaluation criterion:
```

## Decision tests

- **Coordinator Agent:** may call many Agents, but owns one composite, independently testable business result in one lifecycle slice and one human decision boundary.
- **Capability module:** bundles multiple independently accepted results, independent lifecycle transitions, or distinct role-specific allocation/review boundaries. It may contain a coordinator Agent.
- **Orchestrator/service:** routes, retries, passes state, calls tools, or merges data without owning a business result; do not call it an Agent.

Agent and capability module are many-to-many: one module may contain one or more Agents, and one Agent may be reused by multiple modules and role views. Role-specific differences normally belong in permissions, context, framing, and human gates.
