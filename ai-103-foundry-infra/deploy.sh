#!/usr/bin/env bash
# deploy.sh — deploy infra/main.bicep to the pre-created resource group.
#
# Usage:
#   1. Create a .env file next to this script (see README / Exercise 2 Step 2)
#      containing AZURE_RESOURCE_GROUP and AZURE_LOCATION.
#   2. chmod +x deploy.sh
#   3. bash deploy.sh

set -euo pipefail

# Load environment variables from .env (AZURE_RESOURCE_GROUP, AZURE_LOCATION)
if [[ -f ".env" ]]; then
  # shellcheck disable=SC1091
  source .env
else
  echo "ERROR: .env file not found. Create it per Exercise 2 Step 2." >&2
  exit 1
fi

: "${AZURE_RESOURCE_GROUP:?AZURE_RESOURCE_GROUP must be set in .env}"
: "${AZURE_LOCATION:?AZURE_LOCATION must be set in .env}"

echo "Deploying to resource group: $AZURE_RESOURCE_GROUP (location: $AZURE_LOCATION)"

deployment_name="ai103-infra-$(date +%s)"

# TODO 1 (Exercise 2 Step 3): Run `az deployment group create` against infra/main.bicep
#   - --resource-group "$AZURE_RESOURCE_GROUP"
#   - --name "$deployment_name"
#   - --template-file infra/main.bicep
#   - --parameters infra/main.parameters.json
#   - --parameters location="$AZURE_LOCATION"
#   - --output none
echo "NOT IMPLEMENTED — remove this line and implement TODO 1 (az deployment group create)"
exit 1

# TODO 2 (Exercise 2 Step 4): Print the deployment outputs
#   - Use `az deployment group show` with
#       --query "properties.outputs.{foundry:foundryEndpoint.value, search:searchEndpoint.value, storage:storageAccountName.value, appInsights:applicationInsightsConnectionString.value}"
#       -o jsonc
