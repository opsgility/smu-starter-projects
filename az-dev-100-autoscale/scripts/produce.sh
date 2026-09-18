#!/usr/bin/env bash
# Push MESSAGE_COUNT messages to the Service Bus queue to drive up ActiveMessageCount.
# Uses the Service Bus REST API via `az rest` with a bearer token — no `az servicebus queue send-message`
# subcommand (which does not exist in the Azure CLI).
#
# Usage: SERVICE_BUS_NAMESPACE=xxx QUEUE_NAME=anchorline-orders MESSAGE_COUNT=500 ./produce.sh

set -euo pipefail

: "${SERVICE_BUS_NAMESPACE:?set SERVICE_BUS_NAMESPACE}"
: "${QUEUE_NAME:=anchorline-orders}"
: "${MESSAGE_COUNT:=500}"

TOKEN=$(az account get-access-token --resource https://servicebus.azure.net --query accessToken -o tsv)

for i in $(seq 1 "$MESSAGE_COUNT"); do
  az rest --method POST \
    --uri "https://${SERVICE_BUS_NAMESPACE}.servicebus.windows.net/${QUEUE_NAME}/messages?api-version=2015-01" \
    --headers "Authorization=Bearer ${TOKEN}" "Content-Type=application/atom+xml;type=entry;charset=utf-8" \
    --body "{\"orderId\":$i,\"customer\":\"anchorline-lab\",\"ts\":\"$(date -u +%FT%TZ)\"}" >/dev/null
  if (( i % 50 == 0 )); then echo "sent $i / $MESSAGE_COUNT"; fi
done
echo "done: $MESSAGE_COUNT messages queued"
