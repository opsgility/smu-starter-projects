#!/usr/bin/env bash
# rollback.sh — restore 100% of traffic to the last-known-good revision.
# Usage:
#   ./scripts/rollback.sh <resource-group> <container-app-name> <last-known-good-revision>
# The bad revision is left active but with 0% traffic so you can inspect its logs.
set -euo pipefail

RG="${1:?resource-group required}"
APP="${2:?container-app name required}"
LKG_REV="${3:?last-known-good revision required}"

echo "Rolling back $APP in $RG — sending 100% traffic to $LKG_REV."

az containerapp ingress traffic set \
    --resource-group "$RG" \
    --name "$APP" \
    --revision-weight "$LKG_REV=100"

echo "Traffic restored. Current state:"
az containerapp ingress traffic show \
    --resource-group "$RG" \
    --name "$APP" \
    -o table

echo
echo "The failed revision is still active with 0% traffic — inspect its logs with:"
echo "  az containerapp logs show -g $RG -n $APP --revision <bad-revision-name> --tail 200"
