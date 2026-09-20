# az-dev-200-landing-zone-capstone

Anchorline Outdoors landing-zone-style workload — the AZ-DEV-200 capstone.

## Layout

```
modules/
  network/vnet.bicep            # hub-and-spoke VNet with 3 subnets
  monitoring/workspace.bicep    # Log Analytics + App Insights (workspace-based)
  identity/keyvault.bicep       # RBAC-enabled Key Vault
  data/sqlserver.bicep          # SQL logical server + serverless Gen5 DB, AAD-only auth
  app/webapp.bicep              # Linux P1v3 Web App on .NET 10, MI enabled
envs/
  dev/main.bicep                # single-region trim, B1 SKU
  prod/main.bicep               # multi-region (eastus2 + westus3), P1v3 SKUs
  prod/prod.bicepparam
.github/workflows/
  ship-landing-zone.yml         # test → dev → test → prod, each as a deployment stack
```

## Ship

Merge to `main` triggers:

1. `test-bicep` — bicep lint + PSRule (Azure.Default baseline)
2. `deploy-dev` — what-if + stack create with deny-settings
3. `deploy-test` — approval gate + stack create
4. `deploy-prod` — 2 reviewers + what-if + stack create (multi-region)

## Verify

```bash
az stack group list --resource-group $RG_PROD -o table
az stack group show --name anchorline-prod --resource-group $RG_PROD --query "denySettings.mode"
```

Then hit the two prod web URLs listed in the deployment output.
