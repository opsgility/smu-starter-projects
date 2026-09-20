#!/usr/bin/env bash
# Publish TaskForge landing-zone modules to the private ACR registry.
set -euo pipefail
: "${ACR:?ACR env var required, e.g. ACR=tfacr}"
az acr login -n "$ACR"
bicep publish infra/modules/network.bicep    --target "br:${ACR}.azurecr.io/bicep/network:v1"
bicep publish infra/modules/keyvault.bicep   --target "br:${ACR}.azurecr.io/bicep/keyvault:v1"
bicep publish infra/modules/monitoring.bicep --target "br:${ACR}.azurecr.io/bicep/monitoring:v1"
echo "Published network, keyvault, monitoring modules to br:${ACR}.azurecr.io/bicep/*:v1"
