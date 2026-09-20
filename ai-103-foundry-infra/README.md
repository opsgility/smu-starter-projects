# AI-103 · Lesson 3 · Foundry Infrastructure & Deployments

Starter project for the Summitline Outfitters lead-AI-engineer role. You'll author a
Bicep template for a full Foundry stack, deploy it with a shell script, and wire it
into GitHub Actions with OIDC federated credentials — no client secrets, ever.

## Scenario

Summitline Outfitters (an outdoor-gear retailer) is standing up the infrastructure
backbone for its AI concierge platform. Before any agent code ships, the platform
team needs a declarative, source-controlled Foundry environment:

- A Foundry **AI Services account** (the hub, `kind: AIServices`, `sku: S0`)
- A Foundry **project** as a child of the hub
- **Azure AI Search** (basic SKU) for product-catalog RAG
- A **Storage account** for document uploads
- **Application Insights** + **Log Analytics** for tracing

This starter gives you the skeleton. You fill in the six `TODO` blocks, deploy, and
then CI/CD it.

## Files

| Path | Purpose |
| --- | --- |
| `infra/main.bicep` | Skeleton with six inline `TODO` blocks (Exercise 1). |
| `infra/main.parameters.json` | Sets `hubName: ai103-hub`, `projectName: ai103-project`. |
| `deploy.sh` | Sources `.env`, runs `az deployment group create`, prints outputs (Exercise 2). |
| `.env.example` | Template for the `.env` file `deploy.sh` reads. |
| `.github/workflows/deploy.yml` | Workflow stub for OIDC-based GitHub Actions deploy (Exercise 3). |
| `.gitignore` | Keeps `.env` and Bicep build artifacts out of git. |

## Exercises at a glance

1. **Finish `infra/main.bicep`** — complete `TODO 1..6` (Log Analytics, App Insights,
   Storage, AI Search, Foundry hub, Foundry project, four outputs). Verify with
   `az bicep build --file infra/main.bicep`.
2. **Deploy with `deploy.sh`** — create `.env`, implement both `TODO`s in
   `deploy.sh`, run `bash deploy.sh`, confirm the outputs JSON block.
3. **GitHub Actions workflow** — finish `.github/workflows/deploy.yml`:
   `workflow_dispatch` + `push`, `permissions: id-token: write`, `azure/login@v2`
   with federated credentials, `az deployment group create`, show outputs.

## Quick start (after completing Exercise 1)

```bash
# In the VS Code Server terminal inside the lab:
cd ai-103-foundry-infra

cat > .env <<EOF
AZURE_RESOURCE_GROUP=$(az group list --query "[0].name" -o tsv)
AZURE_LOCATION=eastus2
EOF

chmod +x deploy.sh
bash deploy.sh
```

## Environment expectations

- Region: `eastus2` (policy-enforced — do not change).
- Resource group: pre-created by the lab. `az group list --query "[0].name" -o tsv`
  returns it. Do NOT create a new RG.
- You're signed in as `azureaiuser` (Contributor at subscription, Owner at the RG).
- Bicep + az CLI are pre-installed in the lab VS Code container.

## Expected outputs

After a successful deploy you will see:

- `foundryEndpoint` = `https://ai103-hub.services.ai.azure.com/api/projects/ai103-project`
- `searchEndpoint` = `https://ai103search<suffix>.search.windows.net`
- `storageAccountName` = `ai103sa<suffix>`
- `applicationInsightsConnectionString` = `InstrumentationKey=...`

## Troubleshooting tips

- `Resource type Microsoft.CognitiveServices/accounts/projects is not known` —
  run `az bicep upgrade`.
- `SkuNotSupported` on Search — you used `free`; Search must be `basic`.
- `AADSTS70021` / `No matching federated identity record found` — the federated
  credential subject must exactly match `repo:<org>/<repo>:ref:refs/heads/main`.
- `Unable to get ACTIONS_ID_TOKEN_REQUEST_URL` — `permissions: id-token: write`
  is missing from the workflow.
- `StorageAccountAlreadyTaken` / `hubName already exists` — change `hubName`
  in `infra/main.parameters.json` to `ai103-hub-<yourinitials>`.

## References

- <https://learn.microsoft.com/azure/ai-foundry/how-to/create-resource-template>
- <https://learn.microsoft.com/azure/templates/microsoft.cognitiveservices/accounts>
- <https://learn.microsoft.com/azure/templates/microsoft.search/searchservices>
- <https://learn.microsoft.com/azure/developer/github/connect-from-azure-openid-connect>
