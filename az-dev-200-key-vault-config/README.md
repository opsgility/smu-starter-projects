# az-dev-200-key-vault-config

Anchorline Outdoors — deploy a Key Vault, seed three secrets, wire an App Configuration store with feature flags, and provision an App Service that reads its settings via Key Vault references and App Config.

## Files

- `main.bicep` — one template that provisions Key Vault, seeds secrets from `@secure` params, provisions App Configuration + a feature flag, provisions a Web App with Key Vault reference app settings, and grants the Web App's MI both `Key Vault Secrets User` and `App Configuration Data Reader`.
- `dev.bicepparam` — pulls secrets from env vars via `readEnvironmentVariable()` so the deploy never sees plaintext in source control.

## Deploy

```bash
export DB_CONN_STR="Server=tcp:...;..."
export SB_CONN_STR="Endpoint=sb://...;..."
export COG_KEY="<real-key>"
az deployment group create -g $RG -f main.bicep -p dev.bicepparam
```

## Verify

```bash
WEB=$(az deployment group show -g $RG -n <deployment> --query properties.outputs.webName.value -o tsv)
az webapp config appsettings list -g $RG -n $WEB \
  --query "[?starts_with(value,'@Microsoft.KeyVault')].{name:name, value:value}" -o table
```
