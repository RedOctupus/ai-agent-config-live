# Windows Winget PATH Quirk

After installing `gh` via winget (`winget install --id GitHub.cli`), the executable lands at:

```
C:\Program Files\GitHub CLI\gh.exe
```

**Git-bash sessions started before the install will NOT have this on PATH.** Use the full path:

```bash
"/c/Program Files/GitHub CLI/gh.exe" auth status
"/c/Program Files/GitHub CLI/gh.exe" repo list
```

New git-bash windows will pick up the PATH automatically after the install. To make it available immediately without restarting:

```bash
export PATH="/c/Program Files/GitHub CLI:$PATH"
```

Same pattern applies to any CLI tool installed via winget while a git-bash session is running.
