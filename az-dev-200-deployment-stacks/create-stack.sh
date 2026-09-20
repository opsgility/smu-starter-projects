#!/usr/bin/env bash
# Convert an Anchorline workload to a deployment stack with deny-settings.
# Requires: az cli 2.61+, an authenticated login with Contributor + User Access Administrator on the target scope.
set -euo pipefail

: "${RG:?Set RG to the sandbox resource group name}"
STACK=anchorline-stack-demo

echo "Creating deployment stack '${STACK}' in RG '${RG}' with deny-settings 'denyDelete'..."

az stack group create \
  --name "${STACK}" \
  --resource-group "${RG}" \
  --template-file main.bicep \
  --action-on-unmanage deleteAll \
  --deny-settings-mode denyDelete \
  --deny-settings-apply-to-child-scopes \
  --yes

echo ""
echo "Verifying stack state..."
az stack group show --name "${STACK}" --resource-group "${RG}" \
  --query "{name:name, provisioningState:provisioningState, denyMode:denySettings.mode, actionOnUnmanage:actionOnUnmanage.resources}" \
  -o table
