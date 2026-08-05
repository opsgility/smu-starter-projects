# APL-3016 - Halcyon Assist Copilot Starter

Single shared starter project for **APL-3016 (Build a Custom Copilot on Azure AI Foundry)**.
Used across all five hands-on labs in the course: Lessons 4, 6, 8, 10, and 11.

## Scenario

**Halcyon Insurance** is a mid-market property-and-casualty carrier that writes
homeowners, auto, and umbrella policies. Their customer-service org fields a
few thousand policy questions a day - "Am I covered if a tree falls on the
shed?", "What's my deductible?", "Do you cover water backup?" - and answering
them well requires reading the policy document and matching the language to
the customer's situation.

Across the course you build **Halcyon Assist**, a Copilot that agents can
consult to draft a customer-safe answer grounded in Halcyon's own policy
library. Each lesson layers one capability on top of the same codebase in this
folder: the raw chat client (Lesson 4), Azure AI Search retrieval (Lesson 6),
prompt engineering and tone (Lesson 8), evaluation with the Azure AI
Evaluation SDK (Lesson 10), and observability with Application Insights
(Lesson 11).

## Files

```
apl-3016-copilot/
  README.md
  .env.example              # Filled during Lesson 2, re-hydrated by ARM in later lessons.
  .gitignore
  requirements.txt          # Manifest only - packages are already installed in the lab container.
  src/
    verify_env.py           # Smoke test - reads .env, one chat.completions call.
    copilot_agent.py        # Halcyon Assist agent skeleton (Microsoft Agent Framework).
    rag_client.py           # AI Search wiring - filled in during Lesson 6.
    capture_golden.py       # Turns data/golden-inputs.txt into golden JSONL for eval.
    eval_runner.py          # RelevanceEvaluator + GroundednessEvaluator + FluencyEvaluator.
  data/
    golden-inputs.txt       # One prompt per line - filled during Lesson 10.
    policies/
      halcyon-homeowners.md
      halcyon-auto.md
      halcyon-umbrella.md
```

## Scripts

- `src/verify_env.py` - reads `.env`, creates an `AIProjectClient` with
  `DefaultAzureCredential`, sends one chat completion to
  `AZURE_AI_CHAT_DEPLOYMENT`, prints the reply. Use this to confirm your
  Foundry project + model deployment + role assignment are wired up.
- `src/copilot_agent.py` - the Halcyon Assist agent. Bare-minimum single-turn
  conversation on the chat deployment. Extended lesson by lesson.
- `src/rag_client.py` - placeholder that Lesson 6 fills in. Wires the Foundry
  AI Search tool onto the agent so it can ground answers in the `halcyon-policies`
  index.
- `src/capture_golden.py` - reads `data/golden-inputs.txt` one prompt per
  line, runs each through the current agent, writes
  `data/aurora-eval-golden.jsonl` in the shape the evaluation SDK expects.
- `src/eval_runner.py` - thin wrapper around `azure.ai.evaluation` that runs
  `RelevanceEvaluator`, `GroundednessEvaluator`, and `FluencyEvaluator` over
  the golden JSONL and prints aggregate scores.

## How to run

The lab platform signs you in to Azure as the `azureaiuser` credential (has
`Azure AI User` on the Foundry project and `Search Index Data Reader` on the
AI Search resource). No API keys are used - every script goes through
`DefaultAzureCredential`.

1. Copy `.env.example` to `.env` (Lesson 2 walks through this) and fill in
   the values from the ARM deployment outputs.
2. Confirm the environment:

   ```bash
   python src/verify_env.py
   ```

3. Run the agent skeleton:

   ```bash
   python src/copilot_agent.py
   ```

## Packages

Every package in `requirements.txt` is **already preinstalled** in the
`python-ai` VS Code Server container the lab runs in - `azure-ai-projects`,
`azure-identity`, `agent-framework`, `agent-framework-foundry`,
`azure-ai-evaluation[remote]`, `azure-search-documents`, `azure-storage-blob`,
`azure-monitor-opentelemetry`, `python-dotenv`, and `rich`. You do **not** run
`pip install` at lab time. The `requirements.txt` in this folder is kept as a
manifest for reference and for local development outside the lab.

## Authentication

Every code path in this starter uses `DefaultAzureCredential`. No keys are
hardcoded and no keys are read from `.env`. The `azureaiuser` account that
`az login` picks up in the lab holds every role the code needs.

## Notes

- Model deployment names always come from `AZURE_AI_CHAT_DEPLOYMENT`,
  `AZURE_AI_CHAT_MINI_DEPLOYMENT`, and `AZURE_AI_EMBEDDING_DEPLOYMENT`. Never
  hardcode a model name in the source.
- `data/policies/` ships three short sample policy documents used by Lesson 6
  to seed the AI Search index. They are realistic-looking but fictional
  Halcyon Insurance policy language.
