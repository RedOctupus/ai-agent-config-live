# Agent boundary

## Agent contract

```text
Name:
Business result owned:
Lifecycle stage:
Inputs:
Outputs:
Collaborators:
Atomic capabilities:
Memory read:
Memory write:
Human confirmation:
Failure/conflict handling:
Evaluation criterion:
```

## Boundary tests

An Agent is probably too broad when it owns unrelated lifecycle transitions, has no single result, or requires every project domain. It is probably too narrow when it only wraps one query, formatter, or API call and has no independent business evaluation.

The same Agent may be called from multiple role views. Role-specific differences belong in permissions, context, output framing, and human gates unless the business result itself differs.
