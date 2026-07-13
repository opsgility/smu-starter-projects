# AI-3016 · RAG & Evaluation starter (`intel-rag-eval`)

Scenario: **Sentinel Intelligence Bureau (SIB)** — you are the lead AI engineer
on the OSINT Modernization team, grounding the analyst-facing OSINT Concierge
on the bureau's internal handbook + policy collection. SIB legal requires
groundedness and relevance scores of at least **3.5** on the evaluation set
before the Concierge ships to analysts.

All sample data is non-classified, fictional, and synthesized for training.

This starter project contains the skeleton files for the three lab exercises
in the RAG & Evaluation lessons of **Azure AI Foundry Intensive for DIA
Developers (AI-3016)**. Each exercise asks you to replace marked `TODO`
blocks with code from the exercise instructions.

## Files

```
intel-rag-eval/
├── app/
│   ├── __init__.py
│   ├── retrieval.py      # Ex 1: create_index / Ex 2: ingest + search
│   ├── main.py           # Ex 3: FastAPI /chat endpoint (RAG)
│   └── evaluate.py       # Ex 3: chat_target + evaluate() with groundedness/relevance
├── sample_docs/          # Sentinel Intelligence Bureau OSINT handbook + policies (Markdown)
├── eval_data.jsonl       # 5 evaluation questions
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Infrastructure

The lab's ARM template pre-deploys all required Azure resources into the
lab resource group. You do **not** deploy Bicep or ARM yourself — just
capture the outputs (Exercise 1, Step 4):

- Foundry AI Services account + project (`sib-osint-rag`)
- `gpt-5-mini` deployment (chat)
- `text-embedding-3-small` deployment (1536-dim embeddings)
- Azure AI Search (Basic SKU — vector + semantic ranker enabled)
- Storage account with a `sib-osint-docs` container

## Setup

Inside the VS Code Server terminal (the workspace is already the starter
root; no `cd` needed). The `python-ai` lab container already has every
package in `requirements.txt` pre-installed at container build time, so no
`pip install` is needed:

```bash
cp .env.example .env
# edit .env with the values captured from `az deployment group show` in Ex 1
```

## Exercise walkthrough

### Exercise 1 — Create the AI Search index

Implement `create_index()` in `app/retrieval.py`. Fields: `id`, `source`, `chunk`,
and a 1536-dim `embedding` vector. HNSW algorithm + `default` vector profile +
`default` semantic configuration with `chunk` as the content field.

```bash
python -c "from app import retrieval; retrieval.create_index(); print('ok')"
```

### Exercise 2 — Ingest, embed, and search `sample_docs`

Implement `ingest()` and `search()` in `app/retrieval.py`. Uses the
pre-implemented `_chunk()` helper (800-char window, 100 overlap) and `_embed()`
helper (Foundry project client → OpenAI embeddings).

```bash
python -m app.retrieval ingest
python -m app.retrieval search "What sources are in scope for the OSINT Concierge?"
```

### Exercise 3 — Build `/chat` and run evaluations

Implement the `/chat` handler in `app/main.py`, and `chat_target()` + `main()`
in `app/evaluate.py`. `evaluate()` scores every row in `eval_data.jsonl` with
`GroundednessEvaluator` and `RelevanceEvaluator`.

```bash
uvicorn app.main:app --reload --port 8000
# in another terminal:
curl -s -X POST http://127.0.0.1:8000/chat -F "message=What sources are in scope?" | python -m json.tool

python -m app.evaluate
```

Open the printed Foundry Studio URL to inspect per-row scores. Aggregate
`groundedness.groundedness` and `relevance.relevance` should both land at or
above **3.5**.
