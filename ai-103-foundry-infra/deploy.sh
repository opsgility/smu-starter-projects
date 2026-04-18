#!/usr/bin/env bash
# Deploys the Foundry stack defined in infra/main.bicep
set -euo pipefail

if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

: "${AZURE_RESOURCE_GROUP:?AZURE_RESOURCE_GROUP must be set}"
: "${AZURE_LOCATION:?AZURE_LOCATION must be set}"

# TODO 1: use az deployment group create --resource-group $AZURE_RESOURCE_GROUP \
#         --template-file infra/main.bicep --parameters infra/main.parameters.json
# TODO 2: on success, print the outputs (foundryEndpoint, searchEndpoint, storageAccount)
#         using az deployment group show --query properties.outputs
echo "NOT IMPLEMENTED — fill in the TODOs above."
exit 1
