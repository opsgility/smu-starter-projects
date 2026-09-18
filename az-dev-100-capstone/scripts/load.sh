#!/usr/bin/env bash
# Generate a mixed load against the Anchorline capstone storefront so autoscale + KQL have data.
# Usage: ./scripts/load.sh https://<host> [duration-seconds] [rps]
#
# Effective throughput is lower than the nominal RPS because the outer loop
# includes a `sleep 1` between batches. At RPS=20, expect ~15 rps effective
# and ~5,400 requests over 6 minutes.

set -euo pipefail
HOST="${1:?Usage: $0 <base-url> [duration] [rps]}"
DURATION="${2:-120}"
RPS="${3:-5}"

end=$(( $(date +%s) + DURATION ))
count=0

echo "Load: $HOST for ${DURATION}s at ~${RPS}rps"

while [ "$(date +%s)" -lt "$end" ]; do
    for _ in $(seq 1 "$RPS"); do
        endpoint=$( ( echo /fast; echo /fast; echo /fast; echo /slow; echo /checkout; echo /checkout; echo /fail ) | shuf -n 1 )
        curl -s -o /dev/null -w "%{http_code} %{time_total}s ${endpoint}\n" "${HOST}${endpoint}" &
        count=$(( count + 1 ))
    done
    wait
    sleep 1
done

echo "Done. Sent ~${count} requests."
