#!/bin/bash
# auto-sync.sh - Auto sync Hermes state to git repo and push
# Called by cron or task scheduler
# Requires: git, gh CLI authenticated

set -e

HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
REPO_DIR="$HOME/ai-agent-config-live"
LOG_FILE="$HERMES_HOME/logs/auto-sync.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

log "=== Auto-sync started ==="

# 1. Ensure repo is cloned
if [ ! -d "$REPO_DIR/.git" ]; then
    log "Cloning repo..."
    git clone https://github.com/RedOctupus/ai-agent-config-live.git "$REPO_DIR"
fi

cd "$REPO_DIR"
git pull origin main 2>/dev/null || true

# 2. Sync skills
log "Syncing skills..."
rm -rf skills/*/ 2>/dev/null || true
for dir in "$HERMES_HOME/skills"/*/; do
    name=$(basename "$dir")
    case "$name" in
        .*|DESCRIPTION.md) continue ;;
    esac
    cp -r "$dir" "skills/$name" 2>/dev/null || true
done

# Clean metadata
find skills -name ".curator_state" -delete 2>/dev/null || true
find skills -name ".bundled_manifest" -delete 2>/dev/null || true

skill_count=$(find skills -name "SKILL.md" | wc -l)
log "Skills synced: $skill_count"

# 3. Sync memory
log "Syncing memory..."
for f in MEMORY.md USER.md; do
    if [ -f "$HERMES_HOME/memories/$f" ]; then
        base=$(echo "$f" | tr '[:upper:]' '[:lower:]' | sed 's/\.md$//')
        cp "$HERMES_HOME/memories/$f" "memory/${base}.md" 2>/dev/null || true
    fi
done
log "Memory synced"

# 4. Commit if changes exist
if git diff --quiet && git diff --cached --quiet; then
    log "No changes, skipping commit"
else
    git add -A
    git commit -m "auto-sync: $(date '+%Y-%m-%d %H:%M')"
    log "Committed changes"

    # 5. Push
    git push origin main 2>&1 | tee -a "$LOG_FILE"
    log "Push complete"
fi

log "=== Auto-sync finished ==="
