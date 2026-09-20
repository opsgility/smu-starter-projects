#!/usr/bin/env bash
# canary_split.sh — shift 10% of production traffic to the newest revision.
# Usage:
#   ./scripts/canary_split.sh <resource-group> <container-app-name> <old-revision> <new-revision> [new-weight]
# Defaults new-weight to 10 (so old gets 90).
set -euo pipefail

RG="${1:?resource-group required}"
APP="${2:?container-app name required}"
OLD_REV="${3:?old revision name required}"
NEW_REV="${4:?new revision name required}"
NEW_WEIGHT="${5:-10}"
OLD_WEIGHT=$((100 - NEW_WEIGHT))

echo "Setting traffic split on $APP in $RG:"
echo "  $OLD_REV = $OLD_WEIGHT%"
echo "  $NEW_REV = $NEW_WEIGHT%"

az containerapp ingress traffic set \
    --resource-group "$RG" \
    --name "$APP" \
    --revision-weight "$OLD_REV=$OLD_WEIGHT" "$NEW_REV=$NEW_WEIGHT"

echo "Current traffic:"
az containerapp ingress traffic show \
    --resource-group "$RG" \
    --name "$APP" \
    -o table
