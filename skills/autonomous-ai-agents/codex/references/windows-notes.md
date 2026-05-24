# Windows & General Pitfalls

## Deprecated Flag

`--full-auto` is deprecated as of Codex CLI 0.133.0. Use `--sandbox workspace-write` instead.

```bash
# OLD (deprecated)
codex exec --full-auto "task"

# NEW
codex exec --sandbox workspace-write "task"
```

## Git Repo Required

Codex refuses to run outside a git repository. For scratch/throwaway work:

```bash
TMP=$(mktemp -d) && cd "$TMP" && git init && codex exec "prompt"
```

## Windows-Specific

### Shell
Codex uses PowerShell (not bash) on Windows for command execution. The PATH includes the Hermes venv Python, which may have permission issues. Codex will search for alternate Python installations automatically.

### Python on Windows
- The Hermes venv Python may fail with `permission denied` when spawned by Codex
- Codex will fall back to other Python installations it finds (e.g., NVIDIA Nsight, LibreOffice bundled)
- This is typically fine for one-shot tasks

### PTY Required
Always use `pty=true` when invoking codex through Hermes terminal — Codex is an interactive TUI app.

```
terminal(command="codex exec 'prompt'", pty=true)
```

## Sandbox Modes

| Flag | Behavior |
|---|---|
| (default) | Read-only sandbox — can read files but not write |
| `--sandbox workspace-write` | Can write to workspace, /tmp, $TMPDIR |
| `--yolo` | No sandbox, no approvals — fastest but most dangerous |
