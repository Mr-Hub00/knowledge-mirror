#!/usr/bin/env bash
set -euo pipefail

# Required env vars:
#   SRC_URL      - source repo (e.g. https://github.com/Mr-Hub00/mrhub.git)
#   MIRROR_DIR   - path to bare mirror (e.g. /absolute/path/IAMHUB/mirrors/mrhub.git)
# Optional:
#   TARGET_URL   - destination repo to receive the mirror

log() { printf '[%s] %s\n' "$(date +'%Y-%m-%d %H:%M:%S')" "$*"; }

: "${SRC_URL:?Set SRC_URL}"
: "${MIRROR_DIR:?Set MIRROR_DIR}"

# Create mirror if missing
if [ ! -d "$MIRROR_DIR" ]; then
  log "Mirror not found, creating: $MIRROR_DIR"
  mkdir -p "$(dirname "$MIRROR_DIR")"
  git clone --mirror "$SRC_URL" "$MIRROR_DIR"
fi

cd "$MIRROR_DIR"

# Ensure 'origin' points to SRC_URL (fetch-only mirror)
git remote set-url --mirror=fetch origin "$SRC_URL"

# Update from source
log "Fetching updates from origin (source)…"
git remote update --prune

# If a target is provided, ensure a named remote and push
if [ -n "${TARGET_URL:-}" ]; then
  if ! git remote | grep -qx "target"; then
    log "Adding 'target' remote…"
    git remote add target "$TARGET_URL"
  else
    # keep target URL fresh if it changed
    git remote set-url target "$TARGET_URL"
  fi

  log "Pushing mirror to 'target'…"
  git push --mirror target
else
  log "TARGET_URL not set; skipping push."
fi

# Optional tidy (safe in a bare mirror)
git reflog expire --expire=now --all || true
git gc --prune=now --aggressive || true

log "Sync complete."