# az-dev-200-loops-conditionals

Anchorline patterns for dynamic Bicep — array-driven loops, environment-conditional resources, and referencing existing VNets with the `existing` keyword.

## Deploy

```bash
# Dev — 2 storage accounts, no Key Vault, injects dev subnet
az deployment group create -g $RG -f main.bicep -p dev.bicepparam

# Prod — 4 storage accounts, deploys Key Vault, injects prod subnet
az deployment group create -g $RG -f main.bicep -p prod.bicepparam
```

## Verify

```bash
az storage account list -g $RG -o table
az keyvault list -g $RG -o table          # empty in dev, one in prod
az network vnet subnet list -g $RG --vnet-name vnet-anchorline-existing -o table
```
