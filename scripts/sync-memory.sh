#!/bin/bash
# sync-memory.sh - Export Hermes memory to this repo
# Usage: ./scripts/sync-memory.sh
# Run from repo root

set -e

HERMES_MEMORY="${HERMES_HOME:-$HOME/.hermes}/memories"
REPO_MEMORY="$(cd "$(dirname "$0")/.." && pwd)/memory"

echo "=== Exporting memory from $HERMES_MEMORY to $REPO_MEMORY ==="

# Copy memory files (skip lock files)
for f in "$HERMES_MEMORY"/MEMORY.md "$HERMES_MEMORY"/USER.md; do
    if [ -f "$f" ]; then
        base=$(basename "$f" .md)
        echo "  Exporting $base..."
        cp "$f" "$REPO_MEMORY/${base,,}.md"
    fi
done

echo "=== Done ==="
