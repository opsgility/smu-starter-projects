#!/usr/bin/env bash
# One-time setup: register a federated credential on an Entra app registration
# so a GitHub Actions workflow on your repo's main branch can obtain Entra tokens
# without a client secret.
set -euo pipefail

: "${APP_OBJECT_ID:?Set APP_OBJECT_ID to the Entra app registration object id}"
: "${GH_REPO:?Set GH_REPO to owner/repo (e.g. anchorline/infra)}"

az ad app federated-credential create \
  --id "${APP_OBJECT_ID}" \
  --parameters "{
    \"name\": \"github-${GH_REPO//\//-}-main\",
    \"issuer\": \"https://token.actions.githubusercontent.com\",
    \"subject\": \"repo:${GH_REPO}:ref:refs/heads/main\",
    \"description\": \"GitHub Actions main branch deploy\",
    \"audiences\": [ \"api://AzureADTokenExchange\" ]
  }"

echo ""
echo "Verify:"
az ad app federated-credential list --id "${APP_OBJECT_ID}" --query "[].{name:name, subject:subject}" -o table
