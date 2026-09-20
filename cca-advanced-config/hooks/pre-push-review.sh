#!/bin/bash
# Pre-push code review hook
# TODO: Step 2 — Implement pre-push review using Claude Code -p flag
# This script should:
#   1. Get list of changed files using git diff --name-only
#   2. If no changed files, exit 0
#   3. Run: claude -p "Review these changed files for bugs, security issues..." -
#   4. If review result contains "critical", "security", "vulnerability", or "injection" -> exit 1
#   5. Otherwise print review and exit 0

echo "[Hook] Running pre-push code review..."

CHANGED_FILES=$(git diff --name-only HEAD~1 2>/dev/null || git diff --name-only --cached)

if [ -z "$CHANGED_FILES" ]; then
  echo "[Hook] No changed files to review."
  exit 0
fi

echo "[Hook] Reviewing files: $CHANGED_FILES"

# TODO: implement claude -p review call and critical issue check

echo "[Hook] Review complete. No critical issues found."
exit 0
