# AI-103 Lesson 8 — Agent Service Fundamentals (Summitline Concierge)

Starter project for **AI-103 Lab 2255 — Agent Service Fundamentals**. You will
build the `summitline-concierge` agent for **Summitline Outfitters**, a
specialty outdoor-gear retailer, using the `azure-ai-agents` 1.1.0 SDK with
three Python function tools: `get_weather`, `calculate`, and `lookup_inventory`.

## Scenario

Summitline Outfitters sells hiking, climbing, and backcountry gear. The
concierge agent helps customer-support staff answer questions about shipping
weather, bulk-order math, and stock levels without leaving the support tool.
Every more-advanced lesson (FileSearchTool, AzureAISearchTool, ConnectedAgentTool)
builds on the same `AgentsClient + ToolSet` foundation you wire up here.

## Files

- `app/agent.py` — the `build_client()` helper and the `converse()` function
  you implement (TODOs 1–5). System prompt is the Summitline concierge persona.
- `app/functions.py` — three fully-implemented Python tools (`get_weather`,
  `calculate`, `lookup_inventory`) plus the `USER_FUNCTIONS` set that
  `FunctionTool` consumes. **Do not modify** — the Sphinx `:param:` docstrings
  are parsed at runtime to build the tool JSON schemas.
- `test_client.py` — a 3-turn smoke test that drives `converse()` and prints
  the role/text transcript.
- `requirements.txt` — pinned SDK versions (`azure-ai-agents>=1.1.0`,
  `azure-identity>=1.19.0`, `azure-ai-projects>=1.0.0`, `python-dotenv>=1.0.1`).
- `.env.example` — the two environment variables the app reads. Copy to `.env`
  and fill in values from the lab's ARM deployment outputs.
- `.gitignore` — excludes `.env`, `__pycache__/`, `.venv/`, and editor state.

## How to run

The lab's ARM template (Template 21 — Foundry + project + `gpt-4.1-mini`) auto-
deploys when the lab starts, so you do not provision anything yourself.

1. **Sign in to Azure in the VS Code terminal**

   ```bash
   az login
   ```

   Select the `azureaiuser` account shown on the Lab Environment tab.

2. **Install dependencies**

   ```bash
   python -m pip install -r requirements.txt
   ```

3. **Capture the ARM outputs and write `.env`** (see Exercise 1 Step 4)

   ```bash
   RG=$(az group list --query "[0].name" -o tsv)
   DEP=$(az deployment group list --resource-group "$RG" --query "[0].name" -o tsv)
   PROJECT_ENDPOINT=$(az deployment group show --resource-group "$RG" --name "$DEP" \
       --query "properties.outputs.projectEndpoint.value" -o tsv)
   MODEL_DEPLOYMENT_NAME=$(az deployment group show --resource-group "$RG" --name "$DEP" \
       --query "properties.outputs.gpt41MiniDeploymentName.value" -o tsv)
   printf "PROJECT_ENDPOINT=%s\nMODEL_DEPLOYMENT_NAME=%s\n" \
       "$PROJECT_ENDPOINT" "$MODEL_DEPLOYMENT_NAME" > .env
   ```

4. **Implement the TODOs in `app/agent.py`** (Exercises 1 and 2)

5. **Run the smoke test**

   ```bash
   python test_client.py
   ```

   Expected output is four user/assistant pairs — each assistant reply cites
   the tool it used (`get_weather`, `calculate`, or `lookup_inventory`).

## Authentication

`build_client()` uses `DefaultAzureCredential` — keyless auth backed by the
cached `az login` token. No API keys. The `azureaiuser` credential assigned
to the lab holds `Azure AI User` on the Foundry account, which is the only
role the Agents Service needs.

## Notes

- Every call to `converse()` creates a fresh agent and deletes it on exit.
  If a run crashes, list leaked agents with
  `az rest --method GET --url "$PROJECT_ENDPOINT/assistants?api-version=2025-05-01"`.
- The three sample SKUs in `app/functions.py` (`NW-SL-001`, `NW-SL-002`,
  `NW-SL-003`) match the phrasing the exercises use — keep them intact so the
  test conversation hits the inventory tool.
