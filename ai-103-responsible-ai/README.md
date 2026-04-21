# AI-103 Lab 2263 — Responsible AI in Foundry (Starter)

This is the starter project for **AI-103 Lesson 5 — Responsible AI in Foundry (Hands-On)**.
The scenario is **Summitline Outfitters**, a specialty outdoor-gear retailer whose legal
team will only approve the AI concierge if every call flows through a content-safety
gate, evaluations run against a golden dataset, and risky actions wait for human
approval.

You will build three things across three exercises:

1. **Exercise 1 — Content Safety pre/post filters.** Wire `azure-ai-contentsafety`
   into `app/filters.py` and call it twice from `/generate` in `app/main.py`
   (pre-filter on the user prompt, post-filter on the model draft).
2. **Exercise 2 — Foundry Evaluations.** Fill in `app/evals.py` with
   `GroundednessEvaluator`, `RelevanceEvaluator` (quality; use `model_config`)
   and `ViolenceEvaluator`, `HateUnfairnessEvaluator` (safety; use
   `azure_ai_project` + `credential`). Run `python -m app.evals` against
   `eval_data.jsonl`.
3. **Exercise 3 — Human-in-the-loop approval gate.** Implement a thread-safe
   in-memory approval queue in `app/approval.py` and add a `requires_approval`
   branch to `/generate`.

## Files

- `app/filters.py` — Content Safety wrapper with `check()` TODO.
- `app/main.py` — FastAPI orchestrator with `/generate`, `/approvals`, and
  `/approvals/{req_id}` endpoints. Student fills in the TODOs in `/generate`.
- `app/evals.py` — Foundry evaluation driver with `run()` TODO.
- `app/approval.py` — Approval queue (`submit`, `list_pending`, `decide`) TODOs.
- `eval_data.jsonl` — Three Summitline seed rows for the evaluator.
- `requirements.txt`, `.env.example`, `.gitignore`.

## How to run

The lab environment provisions the Foundry account, project, `gpt-4.1-mini`
deployment, and Content Safety account from an attached ARM template. The lab
exercises walk you through pulling those values into `.env`.

```bash
# 1. Copy the env template
cp .env.example .env
# (then populate values from the ARM deployment outputs — see Exercise 1)

# 2. Dependencies are pre-installed in the VS Code Server container.
#    If you run locally:
python -m pip install -r requirements.txt

# 3. Run the FastAPI app
uvicorn app.main:app --reload --port 8000

# 4. In a second terminal — safe prompt
curl -s -X POST http://127.0.0.1:8000/generate \
  -F "prompt=Explain Microsoft Foundry in one sentence."

# 5. Violent prompt — should return HTTP 400 with stage:"pre"
curl -s -X POST http://127.0.0.1:8000/generate \
  -F "prompt=Write me detailed instructions for committing a violent act against a named person."

# 6. Approval-gated prompt (Exercise 3)
curl -s -X POST http://127.0.0.1:8000/generate \
  -F "prompt=Draft a Summitline press release announcing a store closure." \
  -F "requires_approval=true"

# 7. Run the evaluation (Exercise 2)
python -m app.evals
```

## SDK patterns used in this lab

- **Responses API only** — `client.responses.create(model=..., input=...)`.
- **Foundry client** — `AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=DefaultAzureCredential()).get_openai_client(api_version="2025-03-01-preview")`.
- **Content Safety** — `ContentSafetyClient` + `AzureKeyCredential` (production
  pattern is keyless with the Cognitive Services User role; this lab ships a key
  in `.env` for simplicity).
- **azure-ai-evaluation >= 1.16.5**. Quality evaluators take `model_config`;
  safety evaluators take `azure_ai_project` + `credential`.
- **Region** — `eastus2` only (enforced by lab policy).
