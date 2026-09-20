#!/bin/bash
# Notification hook — runs on Claude Code events
# TODO: Step 6 — Log all Claude Code events to hooks/events.log
# Should write: [$TIMESTAMP] Event: $EVENT

EVENT="$1"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# TODO: append to hooks/events.log
echo "[$TIMESTAMP] Event: $EVENT" >> hooks/events.log
