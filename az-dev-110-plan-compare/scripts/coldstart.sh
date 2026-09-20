#!/usr/bin/env bash
# Measure cold-start latency by hitting an endpoint after known idle windows.
# Usage: ./scripts/coldstart.sh <base-url> <function-key> [samples] [idle-minutes]

set -euo pipefail
URL="${1:?Usage: $0 <base-url> <function-key> [samples] [idle-min]}"
KEY="${2}"
SAMPLES="${3:-10}"
IDLE_MIN="${4:-3}"

echo "URL=$URL"
echo "Samples=$SAMPLES  Idle between=${IDLE_MIN}min"
echo

for i in $(seq 1 "$SAMPLES"); do
    START=$(date +%s.%N)
    curl -s -o /tmp/resp.json -w "%{http_code}" "$URL/api/ping?code=$KEY" >/tmp/status
    END=$(date +%s.%N)
    STATUS=$(cat /tmp/status)
    ELAPSED_MS=$(echo "($END - $START) * 1000" | bc | cut -d. -f1)
    PROC_AGE=$(jq -r '.processAge // "n/a"' /tmp/resp.json 2>/dev/null || echo "n/a")
    HOST=$(jq -r '.hostname // "n/a"' /tmp/resp.json 2>/dev/null || echo "n/a")
    echo "sample $i: HTTP $STATUS elapsed=${ELAPSED_MS}ms processAge=${PROC_AGE}s host=$HOST"
    if [ "$i" -lt "$SAMPLES" ]; then
        echo "  ...idling ${IDLE_MIN} min to allow cold-start on next sample..."
        sleep $((IDLE_MIN * 60))
    fi
done
