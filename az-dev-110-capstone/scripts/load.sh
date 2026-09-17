#!/usr/bin/env bash
# Load-test the capstone pipeline.
# Usage: ./scripts/load.sh <base-url> <function-key> [count] [rps]

set -euo pipefail
URL="${1:?Usage: $0 <base-url> <function-key> [count] [rps]}"
KEY="${2}"
COUNT="${3:-200}"
RPS="${4:-5}"

echo "Sending $COUNT orders at ~${RPS}rps to $URL"
for i in $(seq 1 "$COUNT"); do
    ORDER_ID="AO-$(date +%s%N)-$i"
    curl -s -X POST "$URL/api/orders?code=$KEY" \
        -H "Content-Type: application/json" \
        -d "{\"orderId\":\"$ORDER_ID\",\"customerId\":\"C-$((RANDOM%100))\",\"sku\":\"AO-TENT-2P\",\"quantity\":$((RANDOM%5+1)),\"total\":$((RANDOM%1000+50)).99}" \
        -o /dev/null -w "%{http_code}\n" &
    if [ $((i % RPS)) -eq 0 ]; then
        wait
        sleep 1
    fi
done
wait
echo "Done."
