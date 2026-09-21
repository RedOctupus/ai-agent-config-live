#!/bin/bash
# sync-skills.sh - Pull skills from Hermes to this repo
# Usage (from repo root): ./scaffold/scripts/sync-skills.sh

set -e

HERMES_SKILLS="${HERMES_HOME:-$HOME/.hermes}/skills"
REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
REPO_SKILLS="$REPO_ROOT/materials/skills"

echo "=== Syncing skills from $HERMES_SKILLS to $REPO_SKILLS ==="

mkdir -p "$REPO_SKILLS"

# Remove old skills (keep manifest)
rm -rf "$REPO_SKILLS"/*/

# Copy all skill categories
for dir in "$HERMES_SKILLS"/*/; do
    name=$(basename "$dir")
    # Skip metadata files
    if [ "$name" = ".curator_state" ] || [ "$name" = ".bundled_manifest" ]; then
        continue
    fi
    echo "  Copying $name..."
    cp -r "$dir" "$REPO_SKILLS/$name"
done

# Clean metadata from copied skills
find "$REPO_SKILLS" -name ".curator_state" -delete 2>/dev/null || true
find "$REPO_SKILLS" -name ".bundled_manifest" -delete 2>/dev/null || true

count=$(find "$REPO_SKILLS" -name "SKILL.md" | wc -l)
echo "=== Done: $count skills synced ==="
