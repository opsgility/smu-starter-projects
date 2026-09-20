#!/bin/bash
# Post-tool audit logger for Claude Code
# TODO: Step 4 — Implement the audit log writer
# This script should:
#   1. Capture TOOL_INPUT and TOOL_OUTPUT from arguments
#   2. Generate a UTC timestamp
#   3. Append a log entry to hooks/audit.log

TOOL_INPUT="$1"
TOOL_OUTPUT="$2"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# TODO: write a log entry to hooks/audit.log
# Format: [$TIMESTAMP] Write operation: $TOOL_INPUT
#         Output: <first 200 chars of TOOL_OUTPUT>
#         ---
