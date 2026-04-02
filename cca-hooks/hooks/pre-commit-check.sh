#!/bin/bash
# Pre-commit validation hook for Claude Code
# TODO: Step 3 — Implement the pre-commit validation logic
# This script should:
#   1. Only run checks when the tool input contains "git commit"
#   2. Check for console.log statements in src/ (block if found, unless "// debug-ok")
#   3. Check for TODO comments in src/ (block if found)
#   4. Validate package.json dependencies
#   5. Exit 0 to allow, exit 1 to block

TOOL_INPUT="$1"

# Only check git commit commands
if ! echo "$TOOL_INPUT" | grep -q "git commit"; then
  exit 0
fi

echo "[Hook] Pre-commit validation running..."

# TODO: implement checks 1-4 above

echo "[Hook] Pre-commit validation passed."
exit 0
