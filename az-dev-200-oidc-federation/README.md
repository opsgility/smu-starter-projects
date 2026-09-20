# az-dev-200-oidc-federation

GitHub Actions → Azure via OIDC federated credentials. Zero client secrets in the repo or Actions Secrets store.

## Setup (once)

1. Create an Entra app registration for the CI identity.
2. Grant it Contributor on the sandbox resource group.
3. Register a federated credential — see `configure-federated-credential.sh`.
4. Set repository secrets `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`. **Do NOT set `AZURE_CLIENT_SECRET`.**
5. Set repository variable `RESOURCE_GROUP` to the sandbox RG.

## Deploy

Push a change to `main.bicep` on `main` — the workflow runs, `azure/login@v2` exchanges the GitHub OIDC token for an Entra token, and `azure/arm-deploy@v2` deploys with no secret ever leaving Entra.
