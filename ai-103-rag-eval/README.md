# AI-103 Lesson 7 — RAG & Evaluation starter (`ai-103-rag-eval`)

Scenario: **Summitline Outfitters** — you are the lead AI engineer grounding the
support chat on the company knowledge base. Legal wants groundedness and
relevance scores of at least 3.5 on the evaluation set before the chat ships.

This starter project contains the skeleton files for the three lab exercises in
AI-103 · Lesson 7. Each exercise asks you to replace marked `TODO` blocks with
code from the exercise instructions.

## Files

```
ai-103-rag-eval/
├── app/
│   ├── __init__.py
│   ├── retrieval.py      # Ex 1: create_index / Ex 2: ingest + search
│   ├── main.py           # Ex 3: FastAPI /chat endpoint (RAG)
│   └── evaluate.py       # Ex 3: chat_target + evaluate() with groundedness/relevance
├── sample_docs/          # Summitline Outfitters knowledge base (Markdown)
├── eval_data.jsonl       # 5 evaluation questions
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Infrastructure

The lab's ARM template pre-deploys all required Azure resources into the
lab resource group. You do **not** deploy Bicep or ARM yourself — just capture
the outputs (Exercise 1, Step 4):

- Foundry AI Services account + project
- `gpt-4.1-mini` deployment (chat)
- `text-embedding-3-small` deployment (1536-dim embeddings)
- Azure AI Search (Basic SKU — vector + semantic ranker enabled)
- Storage account with a `summitline-docs` container

## Setup

From the `ai-103-rag-eval` folder:

```bash
python -m venv .venv
source .venv/bin/activate        # Linux / macOS / WSL
# .venv\Scripts\Activate.ps1     # Windows PowerShell
pip install -r requirements.txt
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
python -m app.retrieval search "What is the Summitline return policy?"
```

### Exercise 3 — Build `/chat` and run evaluations

Implement the `/chat` handler in `app/main.py`, and `chat_target()` + `main()`
in `app/evaluate.py`. `evaluate()` scores every row in `eval_data.jsonl` with
`GroundednessEvaluator` and `RelevanceEvaluator`.

```bash
uvicorn app.main:app --reload --port 8000
# in another terminal:
curl -s -X POST http://127.0.0.1:8000/chat -F "message=What is the return policy?" | python -m json.tool

python -m app.evaluate
```

Open the printed Foundry Studio URL to inspect per-row scores. Aggregate
`groundedness.groundedness` and `relevance.relevance` should both land at or
above **3.5**.
