#!/bin/bash
# Post-Bash audit hook
# TODO: Step 4 — Log every bash command execution to an audit trail
# Should append: timestamp, tool input (command), and output summary to hooks/bash-audit.log

TOOL_INPUT="$1"
TOOL_OUTPUT="$2"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# TODO: append log entry to hooks/bash-audit.log
