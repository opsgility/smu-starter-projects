#!/usr/bin/env bash
# After manually mutating a stack-managed resource in the portal,
# use what-if against the stack template to detect drift, then re-apply to remediate.
set -euo pipefail

: "${RG:?}"
STACK=anchorline-stack-demo

echo "Diffing current stack against template (drift detection)..."
az deployment group what-if \
  --resource-group "${RG}" \
  --template-file main.bicep \
  --result-format ResourceIdOnly

echo ""
echo "To remediate, run:"
echo "  az stack group create --name ${STACK} --resource-group ${RG} --template-file main.bicep --action-on-unmanage deleteAll --deny-settings-mode denyDelete --yes"
