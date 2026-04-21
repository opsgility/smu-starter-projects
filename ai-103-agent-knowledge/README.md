# AI-103 Lesson 9 — Knowledge Tools & File Search (Summitline Outfitters)

Starter project for the Summitline Outfitters concierge agent. Across three
exercises you will attach three distinct knowledge surfaces to one Azure AI
Agents Service agent:

1. **Exercise 1 — `FileSearchTool`** backed by a vector store built from
   `sample_data/product-catalog.pdf`. Answers product catalog questions.
2. **Exercise 2 — `AzureAISearchTool`** bound to a Foundry project connection
   that targets the `summitline-kb` index. Answers policy / warranty / FAQ
   questions.
3. **Exercise 3 — custom `FunctionTool`** wrapping Azure AI Content
   Understanding (`extract_invoice`). Answers invoice-extraction questions.

All three tools live on the **same** agent; the model chooses which one to
call based on the agent instructions and each tool's schema.

## Scenario

Summitline Outfitters is a specialty outdoor-gear retailer. Their concierge
agent needs to answer three kinds of questions from one chat surface:

- "Do you carry a 4-season tent under 5 lbs?" (catalog PDF lookup)
- "What is the return policy on seasonal apparel?" (KB policy lookup)
- "Summarize the invoice at `sample_data/invoice.pdf` — vendor, total, line
  items." (structured extraction from an arbitrary PDF)

You are the lead AI engineer. You own the agent's tools.

## Project layout

```
ai-103-agent-knowledge/
  app/
    __init__.py
    agent.py         # build_agent_with_tools() assembles all three tools
    cu_tool.py       # extract_invoice() — Content Understanding REST wrapper
  sample_data/
    product-catalog.pdf   # (supplied by the lab - drop a real PDF here)
    invoice.pdf           # (supplied by the lab - drop a real PDF here)
    summitline-returns.md      # seed doc for the summitline-kb index
    summitline-warranty.md     # seed doc for the summitline-kb index
    summitline-pickup.md       # seed doc for the summitline-kb index
  requirements.txt
  .env.example
  .gitignore
  README.md
```

> `sample_data/product-catalog.pdf` and `sample_data/invoice.pdf` must be
> real PDFs for the Agents Service / Content Understanding calls to succeed.
> See `sample_data/product-catalog.pdf.md` and `sample_data/invoice.pdf.md`
> for what each file is expected to contain.

## Prerequisites

- The lab environment has started. An ARM template auto-deploys a Foundry
  AIServices account, a child project, a `gpt-4.1-mini` deployment, and an
  Azure AI Search service into the pre-created resource group in `eastus2`.
- You signed in to Azure in an earlier lesson and `az account show` returns
  your identity.
- Python 3.11+ available in the lab container.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Copy the environment template and fill it in as each exercise instructs:

```bash
cp .env.example .env
```

The exercises walk you through populating every variable using
`az deployment group show` against the auto-deployment outputs.

## Run

```bash
python -m app.agent
```

Exercise 1 expects a grounded answer to "What products do we sell?".
Exercise 2 adds a grounded answer to "What is our return policy for seasonal
apparel?". Exercise 3 adds a JSON-style response to "Summarize the invoice
in sample_data/invoice.pdf.".

## Authentication

`DefaultAzureCredential` is used everywhere except the Content Understanding
REST calls, which still require the Foundry account's `Ocp-Apim-Subscription-Key`
in `eastus2` (CU AAD support is not yet GA there).
