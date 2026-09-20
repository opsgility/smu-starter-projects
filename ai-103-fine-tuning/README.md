# AI-103 Fine-tuning — Summitline gear-recommendation concierge

Starter project for the AI-103 hands-on lab **"Fine-tuning Foundation Models in
Foundry - Lab Exercises"**. You fine-tune a Foundry Azure OpenAI base model on
Summitline Outfitters' curated gear-recommendation dataset, deploy the
fine-tuned model, and compare it against the base model on held-out Summitline
prompts.

## Scenario

Summitline Outfitters is a specialty outdoor-gear retailer (hiking, climbing,
backcountry). Their support-agent tooling calls a base chat model to suggest
gear for a customer's plan, but the base model recommends off-brand items and
doesn't consistently name Summitline SKUs (pattern `NW-SL-###`). You fine-tune
`gpt-4.1-mini` on ~60 hand-curated Summitline conversations so the concierge
consistently recommends real in-catalog SKUs, keeps the friendly Summitline
tone, and cites the tool it used (weather / calculate / inventory / gear-match)
in one short sentence.

## Base model + region

- **Base model:** `gpt-4.1-mini` version `2025-04-14` (GlobalStandard SKU for
  inference).
- **Fine-tuning method:** SFT (Supervised Fine-Tuning). Verified GA per
  https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure#fine-tuning-models
  (checked 2026-08-23). Global fine-tuning is available from every Azure OpenAI
  region.
- **Fine-tuned model deployment SKU:** `Developer` (24-hour test deployment,
  no hourly hosting fee; per-token billing only). Verified per
  https://learn.microsoft.com/azure/ai-foundry/openai/how-to/fine-tune-test
  (checked 2026-08-23).
- **Region:** `eastus2` (matches pool 6 compute region; both Global training
  and Developer deployment work here).

> **Note:** gpt-5 / gpt-5-mini fine-tuning is not currently offered — gpt-5
> (2025-08-07) supports RFT only and is gated by invitation. Do not swap the
> base model without re-checking MS Learn.

## Files

```
ai-103-fine-tuning/
  README.md
  .env.example                 # ARM outputs the student fills in
  .gitignore
  requirements.txt             # Reference manifest — packages already in the python-ai container
  data/
    gear_recommendations.jsonl # ~60 curated Summitline chat rows (training)
    held_out_test_prompts.json # 12 prompts used by compare_base_vs_finetuned.py
  src/
    verify_env.py              # Smoke test: reads .env, hits base deployment, exits 0/1
    upload_dataset.py          # Exercise 3 — upload the JSONL training file
    start_finetune_job.py      # Exercise 4 — create the SFT job
    poll_job_status.py         # Exercise 5 — poll + print loss / validation metrics
    deploy_finetuned.py        # Exercise 6 — create a Developer-SKU deployment
    compare_base_vs_finetuned.py  # Exercise 7 — side-by-side on held-out prompts
```

## How to run

The lab's ARM template pre-deploys the Foundry account + project + base
`gpt-4.1-mini` deployment when the lab starts (allow up to 10 minutes).

1. **Sign in to Azure in the VS Code terminal**

   ```bash
   az login --use-device-code
   ```

   The container is headless — always use `--use-device-code`. Follow the
   `https://microsoft.com/devicelogin` link and select the `azureaiuser`
   account shown on the Lab Environment tab.

2. **Capture ARM outputs into `.env`** (Exercise 1 Step 4)

   ```bash
   RG=$(az group list --query "[?starts_with(name, 'summitline-finetune')].name | [0]" -o tsv)
   DEP=$(az deployment group list --resource-group "$RG" --query "[0].name" -o tsv)
   AZURE_OPENAI_ENDPOINT=$(az deployment group show --resource-group "$RG" --name "$DEP" \
       --query "properties.outputs.AZURE_OPENAI_ENDPOINT.value" -o tsv)
   BASE_MODEL_DEPLOYMENT=$(az deployment group show --resource-group "$RG" --name "$DEP" \
       --query "properties.outputs.BASE_MODEL_DEPLOYMENT.value" -o tsv)
   AZURE_AI_PROJECT_ENDPOINT=$(az deployment group show --resource-group "$RG" --name "$DEP" \
       --query "properties.outputs.AZURE_AI_PROJECT_ENDPOINT.value" -o tsv)
   AZURE_AI_PROJECT_NAME=$(az deployment group show --resource-group "$RG" --name "$DEP" \
       --query "properties.outputs.AZURE_AI_PROJECT_NAME.value" -o tsv)
   AZURE_STORAGE_ACCOUNT_NAME=$(az deployment group show --resource-group "$RG" --name "$DEP" \
       --query "properties.outputs.AZURE_STORAGE_ACCOUNT_NAME.value" -o tsv)
   cat > .env <<EOF
   AZURE_OPENAI_ENDPOINT=$AZURE_OPENAI_ENDPOINT
   BASE_MODEL_DEPLOYMENT=$BASE_MODEL_DEPLOYMENT
   AZURE_AI_PROJECT_ENDPOINT=$AZURE_AI_PROJECT_ENDPOINT
   AZURE_AI_PROJECT_NAME=$AZURE_AI_PROJECT_NAME
   AZURE_STORAGE_ACCOUNT_NAME=$AZURE_STORAGE_ACCOUNT_NAME
   FINETUNE_JOB_NAME_PREFIX=summitline-concierge
   EOF
   ```

3. **Smoke test the environment** (Exercise 1 Step 5)

   ```bash
   python src/verify_env.py
   ```

   Expects "Environment OK" and one short base-model reply. Any error means
   `.env` is missing a value or `az login` didn't cache a token for the
   Foundry account.

4. **Work through the exercises in order.** Each `src/*.py` file has TODO
   comments that map to specific exercise steps.

## Packages

Every package in `requirements.txt` is **already preinstalled** in the
`python-ai` VS Code container the lab runs in. Do **not** run `pip install`
at lab time. `requirements.txt` is kept as a reference manifest for local
development outside the lab.

## Authentication

All scripts use `DefaultAzureCredential` — keyless auth backed by the cached
`az login` token. No API keys anywhere in the code. The lab's `azureaiuser`
credential holds `Foundry User` + `Cognitive Services OpenAI User` + `Contributor`
at subscription scope; the platform additionally grants `Owner` at the
pre-created resource-group scope so the student can deploy the fine-tuned
model (an Owner-required operation on `Microsoft.CognitiveServices/accounts/deployments`).

Fine-tuning API surface: `openai` Python SDK against the Foundry account's
Azure OpenAI endpoint, using the v1 `AzureOpenAI` client with
`azure_ad_token_provider=`... backed by `DefaultAzureCredential`.

## Notes

- The `data/gear_recommendations.jsonl` file is intentionally small (~60 rows).
  Real fine-tuning needs hundreds to thousands of examples for quality gains —
  the lab intentionally uses a small dataset so the SFT job completes in ~10-15
  minutes rather than hours. Exercise 2 discusses this trade-off.
- The `system` message in every training row establishes the Summitline
  concierge persona — do not rewrite it, and if you add examples, keep the
  same `system` verbatim so the fine-tune learns a single voice.
- `held_out_test_prompts.json` is kept separate from the training set. Do not
  copy any of its user messages into `gear_recommendations.jsonl` — the
  Exercise 7 comparison is only meaningful on prompts the fine-tune never saw.
- Every fine-tuned deployment created in Exercise 6 uses `Developer` SKU with
  a 24-hour lifetime. The lab teardown deletes the deployment automatically,
  but if you want to redeploy mid-lab, `az cognitiveservices account
  deployment delete` the old one first — Developer SKU allows only one
  deployment per fine-tuned model at a time.
- Never hardcode a model name in code — always read from an env var.
  `BASE_MODEL_DEPLOYMENT` for the base, `FINETUNED_MODEL_DEPLOYMENT` (set by
  Exercise 6's `deploy_finetuned.py`) for the fine-tuned model.
