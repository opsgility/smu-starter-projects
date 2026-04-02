#!/bin/bash
# Validate file writes based on path patterns
# TODO: Step 4 — Implement path-specific write validation rules
# Rules:
#   1. Config files (.json, .yaml, .yml, .toml): log that config file detected
#   2. CI/CD files (.github/, .gitlab-ci, Jenkinsfile): block write and exit 1
#   3. Test files (*.test.js, *.test.ts): log that assertions will be verified

TOOL_INPUT="$1"

# Extract file path from tool input
FILE_PATH=$(echo "$TOOL_INPUT" | grep -oP '"file_path"\s*:\s*"([^"]*)"' | head -1 | sed 's/.*"file_path"\s*:\s*"//;s/"//')

if [ -z "$FILE_PATH" ]; then
  exit 0
fi

echo "[Validate] Checking write to: $FILE_PATH"

# TODO: implement rules 1-3 above

exit 0
