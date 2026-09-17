# az-dev-200-bicep-first

Anchorline Outdoors first Bicep template. Provisions a Storage Account, App Service Plan (Linux, B1), and Web App running .NET 10 into a single resource group.

## Files

| File | Purpose |
|---|---|
| `main.bicep` | Resource-group scoped template. Three resources, four decorated parameters, four outputs. |
| `main.bicepparam` | Parameter file (Bicep-native syntax, replaces `parameters.json`). |
| `bicepconfig.json` | Linter rule configuration. |
| `deploy.sh` | One-shot deployment against the pre-provisioned sandbox RG. |

## Run

```bash
chmod +x deploy.sh
./deploy.sh
```

## Verify

```bash
az resource list -g "$RG" -o table
curl -sI $(az deployment group show -g $RG --name <deployment-name> --query properties.outputs.webAppUrl.value -o tsv)
```

Expected: three resources listed (Storage, Plan, Web App); HTTP 200 or 403 from the Web App root (the container is empty; that's fine).
