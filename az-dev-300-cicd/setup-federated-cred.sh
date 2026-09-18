#!/usr/bin/env bash
# Wire GitHub Actions to Azure via OIDC federated credentials.
set -euo pipefail
: "${REPO:?REPO env var required, e.g. REPO=anchorline/taskforge}"
: "${RG_PROD:?RG_PROD env var required}"

az ad app create --display-name "taskforge-cicd" || true
APP=$(az ad app list --display-name taskforge-cicd --query "[0].appId" -o tsv)
az ad sp create --id "$APP" 2>/dev/null || true

for sub in "ref:refs/heads/main" "pull_request" "environment:production"; do
  name=$(echo "$sub" | tr ':/' '--')
  cat > /tmp/fed.json <<EOF
{
  "name": "$name",
  "issuer": "https://token.actions.githubusercontent.com",
  "subject": "repo:$REPO:$sub",
  "audiences": [ "api://AzureADTokenExchange" ]
}
EOF
  az ad app federated-credential create --id "$APP" --parameters @/tmp/fed.json || true
done

PROD_RG_ID=$(az group show -n "$RG_PROD" --query id -o tsv)
az role assignment create --assignee "$APP" --role Contributor --scope "$PROD_RG_ID"

echo "AZURE_CLIENT_ID=$APP"
echo "AZURE_TENANT_ID=$(az account show --query tenantId -o tsv)"
echo "AZURE_SUBSCRIPTION_ID=$(az account show --query id -o tsv)"
echo "Set these three as GitHub repo secrets."
