#!/usr/bin/env bash
# Publish Anchorline shared modules to the private Bicep registry (ACR).
# Requires: az cli, bicep, an authenticated `az login` with AcrPush on the registry.
set -euo pipefail

: "${ACR_LOGIN_SERVER:?Must set ACR_LOGIN_SERVER (e.g. anchoracrXXXXXX.azurecr.io)}"

az acr login --name "${ACR_LOGIN_SERVER%%.*}"

publish() {
  local name="$1"
  local version="$2"
  local bicep="modules/${name}/main.bicep"
  echo "Publishing ${name}:${version}"
  az bicep publish \
    --file "${bicep}" \
    --target "br:${ACR_LOGIN_SERVER}/bicep/modules/${name}:${version}"
}

publish storage     1.2.0
publish keyvault    1.0.0
publish appinsights 1.0.0

echo ""
echo "Verifying — repositories on registry:"
az acr repository list --name "${ACR_LOGIN_SERVER%%.*}" -o table
