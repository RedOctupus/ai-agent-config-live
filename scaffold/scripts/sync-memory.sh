#!/bin/bash
# sync-memory.sh - Export Hermes memory to this repo
# Usage (from repo root): ./scaffold/scripts/sync-memory.sh
# Writes only to memory/hermes/ — never to memory/kit/ (project-memory-kit).

set -e

HERMES_MEMORY="${HERMES_HOME:-$HOME/.hermes}/memories"
REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
REPO_MEMORY="$REPO_ROOT/memory/hermes"

echo "=== Exporting memory from $HERMES_MEMORY to $REPO_MEMORY ==="

mkdir -p "$REPO_MEMORY"

# Copy memory files (skip lock files)
for f in "$HERMES_MEMORY"/MEMORY.md "$HERMES_MEMORY"/USER.md; do
    if [ -f "$f" ]; then
        base=$(basename "$f" .md)
        echo "  Exporting $base..."
        cp "$f" "$REPO_MEMORY/${base,,}.md"
    fi
done

echo "=== Done ==="
