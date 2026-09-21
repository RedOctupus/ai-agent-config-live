#!/bin/bash
# restore.sh - Restore Hermes from this repo backup
# Usage (from repo root): ./scaffold/scripts/restore.sh
# WARNING: This overwrites existing Hermes config and skills!

set -e

HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SKILLS_SRC="$REPO_ROOT/materials/skills"
HERMES_SRC="$REPO_ROOT/materials/hermes"

echo "=== Restoring Hermes from $REPO_ROOT ==="
echo "Target: $HERMES_HOME"
echo ""

# 1. Skills
echo "[1/4] Restoring skills..."
mkdir -p "$HERMES_HOME/skills"
for dir in "$SKILLS_SRC"/*/; do
    name=$(basename "$dir")
    if [ -d "$dir" ] && [ -f "$dir/SKILL.md" ] || [ -f "$dir"/*/SKILL.md ] 2>/dev/null; then
        cp -r "$dir" "$HERMES_HOME/skills/$name"
        echo "  $name"
    fi
done
count=$(find "$HERMES_HOME/skills" -name "SKILL.md" | wc -l)
echo "  $count skills restored"

# 2. Config (ask before overwriting)
echo ""
echo "[2/4] Restoring config..."
if [ -f "$HERMES_HOME/config.yaml" ]; then
    echo "  Existing config found. Copying as config.yaml.repo for review."
    cp "$HERMES_SRC/config.yaml" "$HERMES_HOME/config.yaml.repo"
    echo "  Review config.yaml.repo and merge manually, or run:"
    echo "    cp $HERMES_HOME/config.yaml.repo $HERMES_HOME/config.yaml"
else
    cp "$HERMES_SRC/config.yaml" "$HERMES_HOME/config.yaml"
    echo "  Config restored"
fi

# 3. Persona
echo ""
echo "[3/4] Restoring persona..."
cp "$HERMES_SRC/SOUL.md" "$HERMES_HOME/SOUL.md"
echo "  SOUL.md restored"

# 4. Env template
echo ""
echo "[4/4] Env template..."
cp "$HERMES_SRC/.env.template" "$HERMES_HOME/.env.template"
echo "  .env.template restored (copy to .env and fill in API keys)"

echo ""
echo "=== Restore complete! ==="
echo ""
echo "Next steps:"
echo "  1. cp ~/.hermes/.env.template ~/.hermes/.env"
echo "  2. Edit ~/.hermes/.env with your API keys"
echo "  3. Edit ~/.hermes/config.yaml if using config.yaml.repo"
echo "  4. Run: hermes doctor"
echo "  5. Start: hermes"
