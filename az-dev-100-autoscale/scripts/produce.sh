#!/usr/bin/env bash
# Push MESSAGE_COUNT messages to the Service Bus queue to drive up ActiveMessageCount.
# Usage: SERVICE_BUS_NAMESPACE=xxx QUEUE_NAME=anchorline-orders MESSAGE_COUNT=500 ./produce.sh

set -euo pipefail

: "${SERVICE_BUS_NAMESPACE:?set SERVICE_BUS_NAMESPACE}"
: "${QUEUE_NAME:=anchorline-orders}"
: "${MESSAGE_COUNT:=500}"

for i in $(seq 1 "$MESSAGE_COUNT"); do
  az servicebus queue send-message \
    --namespace-name "$SERVICE_BUS_NAMESPACE" \
    --queue-name "$QUEUE_NAME" \
    --body "{\"orderId\":$i,\"customer\":\"anchorline-lab\",\"ts\":\"$(date -u +%FT%TZ)\"}" >/dev/null
  if (( i % 50 == 0 )); then echo "sent $i / $MESSAGE_COUNT"; fi
done
echo "done: $MESSAGE_COUNT messages queued"
