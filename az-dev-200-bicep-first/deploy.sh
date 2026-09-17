#!/usr/bin/env bash
# Deploy main.bicep to the sandbox resource group.
# Requires: az cli, bicep, an authenticated `az login`.
set -euo pipefail

RG="${RG:-$(az group list --query "[?starts_with(name,'RG-')].name" -o tsv | head -n1)}"
LOC="${LOC:-eastus2}"

echo "Deploying to RG=$RG in $LOC"

az bicep build --file main.bicep

az deployment group create \
  --resource-group "$RG" \
  --template-file main.bicep \
  --parameters main.bicepparam \
  --name "anchorline-first-$(date +%s)"

echo ""
echo "Deployment outputs:"
az deployment group show \
  --resource-group "$RG" \
  --name "$(az deployment group list --resource-group $RG --query '[0].name' -o tsv)" \
  --query properties.outputs
