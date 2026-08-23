# AI-500 Lesson 5 — Advanced prompts, dynamic context, and multi-agent RAG

Skeleton for the Lesson 5 hands-on lab of AI-500. Ridgevault Financial's platform-team student
writes advanced system prompts for two agents (`portfolio_analyst`, `investment_researcher`),
builds a dynamic-context builder that trims the running thread to a token budget, and wires up
Foundry IQ (Azure AI Search) RAG grounded on a small Ridgevault research library so
`investment_researcher` answers questions with citations from Ridgevault's own docs.

## Scenario

Ridgevault Financial runs a multi-agent advisory platform. Two agents matter for this lab:

- **`portfolio_analyst`** owns Ridgevault client portfolios — allocation, drift, rebalancing signals.
- **`investment_researcher`** answers open-ended research questions — sector outlooks, market
  briefs, the "why" behind a recommendation.

Two problems ship this lesson:

1. The bare model produces generic hedge-fund tropes ("diversify, rebalance, dollar-cost average")
   when Ridgevault's House View wants tighter, opinionated answers. You fix that with an advanced
   persona + few-shot system prompt.
2. `investment_researcher` cites vague "industry sources" that Ridgevault Compliance can't audit.
   You fix that by indexing Ridgevault's own research library into Azure AI Search and wiring
   Foundry IQ RAG grounding so every claim carries a document citation.

## Files

```
ai-500-prompts-rag/
  README.md
  .env.example              # Foundry + AI Search + Storage endpoints. All keyless.
  .gitignore
  requirements.txt          # Reference manifest — every package is already in the lab container.
  src/
    verify_env.py           # 30-line smoke test — reads .env, one auth+model round-trip.
    agents/
      investment_researcher.py   # Agent skeleton. Exercises 2 + 5 fill the system prompt + RAG hook.
    context_builder.py      # Dynamic context builder. Exercise 3 trims to a token budget.
    rag/
      index_docs.py         # Reads data/research/*.md, chunks, embeds, uploads to AI Search.
      foundry_iq_query.py   # Queries the index and returns grounded snippets.
  data/
    research/
      ridgevault-market-brief.md    # Seed doc — Q4 market brief in Ridgevault's House View voice.
      ridgevault-sector-outlook.md  # Seed doc — sector rotation table + rationales.
```

## How to run

1. Sign in with a device code so the container (which has no browser) can complete Entra auth:

   ```
   az login --use-device-code
   ```

2. Copy the env template. The lab environment prints the six values you fill in on the Environment tab:

   ```
   cp .env.example .env
   ```

3. Confirm your identity + deployment reach Foundry:

   ```
   python src/verify_env.py
   ```

   Expect `OK: <model> replied: ...`. If it complains about placeholders, edit `.env`; if it 401s,
   verify `azureaiuser` carries the **Foundry User** + **Cognitive Services OpenAI User** roles at
   subscription scope (the lab environment grants both automatically).

4. Work through the exercises in order. Each exercise TODOs one file:

   - Exercise 2 → `src/agents/investment_researcher.py` system prompt block
   - Exercise 3 → `src/context_builder.py` `trim_to_budget()` function
   - Exercise 4 → `src/rag/index_docs.py` upload loop
   - Exercise 5 → `src/agents/investment_researcher.py` RAG grounding hook
   - Exercise 6 → run `python -m src.agents.investment_researcher` and ask a Ridgevault portfolio
     question that requires grounding.

## Authentication

Every reach for Foundry, Azure AI Search, and Azure Storage goes through
`DefaultAzureCredential` — no API keys ever touch the code. The lab environment binds credential
`azureaiuser` to these roles at subscription scope:

- **Foundry User** — call the Foundry project + models.
- **Cognitive Services OpenAI User** — data-plane calls to model deployments.
- **Search Service Contributor** + **Search Index Data Contributor** + **Search Index Data Reader** —
  create the index, upload documents, and query.
- **Storage Blob Data Contributor** + **Storage Blob Data Reader** — read seed docs from the
  provisioned Storage container.

## Notes

- **Do not run `pip install`.** The `python-ai` container variant already ships `openai`,
  `azure-identity`, `azure-search-documents`, `azure-storage-blob`, `python-dotenv`, and `tiktoken`.
  `requirements.txt` is a reference manifest so local dev works if you clone outside the lab.
- **Never hardcode the model name.** Always read from `os.environ["FOUNDRY_MODEL"]`. Model
  versions change; the env-var indirection keeps the code future-proof.
- **`verify_env.py` refuses to run if `.env` still contains `<angle-bracket>` placeholders.**
  That's on purpose — a clean "OK" from `verify_env` means you have a real deployment.
- **Seed data lives in `data/research/`.** Ridge (the left-sidebar helper) references the two
  file names verbatim — do not rename them. If Exercise 6 asks a question that isn't answered
  by either doc, RAG returns no citations by design, and Ridge will nudge you to add a third
  seed doc rather than let the model hallucinate.
