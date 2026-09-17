#!/usr/bin/env bash
# Generate a mixed load against the Anchorline storefront so KQL has data to query.
# Usage: ./scripts/load.sh https://<host> [duration-seconds] [rps]

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
