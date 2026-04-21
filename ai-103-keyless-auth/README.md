# Summitline Outfitters Concierge — Keyless Auth Starter

Starter project for **AI-103 Lab 2258 — Lesson 4, Manage, Monitor, Secure AI (Hands-On)**.

## Scenario

You are the lead AI engineer at **Summitline Outfitters**, a specialty
outdoor-gear retailer rolling out an AI concierge on Azure AI Foundry. The
team shipped a FastAPI prototype that authenticates to Azure OpenAI with a
static API key (`AZURE_OPENAI_API_KEY`). Your job across the three exercises
in this lab is to migrate the app to **keyless** authentication using
`DefaultAzureCredential`, provision the production identity
(user-assigned managed identity) with Bicep, and prove the role assignment
works end-to-end against the pre-deployed Foundry hub.

The lab environment auto-deploys the Foundry AI Services account, one
child project, and a `gpt-4.1` deployment via ARM template. You do NOT
create those resources in any exercise — you migrate the app that talks
to them.

## Layout

```
ai-103-keyless-auth/
  app/
    __init__.py
    main.py                   # LEGACY key-based FastAPI — rewritten in Ex 1
  bicep/
    identity.bicep            # UAMI + role assignment skeleton — Ex 2 TODOs
    identity.parameters.json  # hubName + location parameters
  requirements.txt
  .env.example
  .gitignore
  README.md
```

## Exercises

1. **Exercise 1 — Migrate `app/main.py` from API key to `DefaultAzureCredential`.**
   Replace the `AzureOpenAI(api_key=...)` client with `AIProjectClient` +
   `DefaultAzureCredential` + `get_openai_client()` and switch the handler
   to `responses.create(input=...)`.

2. **Exercise 2 — Author and deploy `bicep/identity.bicep`.**
   Fill in the three TODOs (UAMI resource, `existing` hub reference, role
   assignment for Azure AI User role `53ca6127-db72-4b80-b1b0-d745d6d5456d`)
   and wire up the `identityClientId` / `identityPrincipalId` outputs.

3. **Exercise 3 — Verify the role assignment and call the Foundry endpoint keyless.**
   Audit the assignment via `az role assignment list`, set `AZURE_CLIENT_ID`
   to the UAMI's `clientId`, and hit `/chat` without any API key anywhere.

## Running the app

From within `ai-103-keyless-auth/`:

```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env
# populate .env from the baseline ARM deployment outputs (Ex 1 step 3)
uvicorn app.main:app --reload --port 8000
```

Then exercise the endpoint:

```bash
curl -s -X POST http://127.0.0.1:8000/chat \
  -d "message=Recommend three lightweight tents for the Pacific Northwest."
```

Expected response shape: `{"reply": "..."}`

## Notes on the migration

- After Exercise 1 completes, `grep -rin "api_key\|AZURE_OPENAI_API_KEY" app/ .env` should print nothing.
- `DefaultAzureCredential`'s chain order is Environment → WorkloadIdentity → ManagedIdentity → SharedTokenCache/VisualStudio → AzureCli → AzurePowerShell → InteractiveBrowser. In the VS Code Server lab container the IMDS step is unavailable, so authentication falls through to `AzureCliCredential` (`az login` from Lesson 2).
- In production (Azure Container Apps with the UAMI attached), setting `AZURE_CLIENT_ID` to the UAMI's `clientId` directs `ManagedIdentityCredential` at that specific identity — no code changes.
- The correct built-in role for Foundry data-plane model calls is **Azure AI User** (`53ca6127-db72-4b80-b1b0-d745d6d5456d`), scoped to the AI Services account (hub). Not `Cognitive Services OpenAI User` — that's the legacy role for standalone `kind: 'OpenAI'` resources.
