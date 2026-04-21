# Summitline Outfitters - Retrieval & Information Extraction

Starter project for **AI-103 Lesson 13 / Lab 2273** (`ai-103-ingest-extract`).

You play an ML platform engineer at **Summitline Outfitters**, a mountain-sports
retailer. Thousands of supplier invoices, vendor contracts, warranty statements
and trail-guide PDFs sit in blob storage. Over four exercises you stand up a
keyless extract -> chunk -> embed -> index -> query pipeline on Azure.

## Architecture

```
    ai103-source blob container
               |
               v
    +-----------------------+       +------------------------+
    | Content Understanding | ----> | text-embedding-3-large |
    |  (summitline-docs)    |       |     (3072-dim)         |
    +-----------------------+       +------------------------+
               |                               |
               v                               v
    +---------------------------------------------------+
    |  Azure AI Search - summitline-knowledge index     |
    |  HNSW vector field + semantic configuration       |
    +---------------------------------------------------+
               ^                               ^
               |                               |
         pipeline.ingest                 pipeline.query
                                               |
                                               v
                                      +-----------------+
                                      | FastAPI  /search|
                                      |          /chat  |
                                      +-----------------+
```

## Layout

```
ai-103-ingest-extract/
├── pipeline/
│   ├── __init__.py
│   ├── cu_extract.py     # Exercise 1: analyzer lifecycle + extract()
│   ├── ingest.py         # Exercise 2: main() pipeline loop
│   ├── index.py          # Exercise 3: ensure_index()
│   └── query.py          # Exercise 4: query(), cite(), CLI
├── app/
│   ├── __init__.py
│   └── main.py           # FastAPI /search and /chat endpoints
├── sample_data/          # Summitline source documents (uploaded in Ex 2)
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Exercises

| # | File                 | You implement                                              |
|---|----------------------|------------------------------------------------------------|
| 1 | `pipeline/cu_extract.py` | `SCHEMA`, `ensure_analyzer()`, `extract()` polling loop |
| 2 | `pipeline/ingest.py`     | `main()` - list blobs, extract, chunk, embed, upload    |
| 3 | `pipeline/index.py`      | `ensure_index()` - HNSW vector + semantic config        |
| 4 | `pipeline/query.py`      | `cite()` helper + CLI entry-point                       |

`_chunk()` and `_embed()` in `ingest.py`, and `query()` in `query.py`, are
already implemented so you can focus on the exercise-specific code.

## Lab infrastructure (pre-deployed via ARM)

The lab platform deploys the stack before you start. Pull the values you need
into `pipeline/.env`:

```bash
RG=$(az group list --query "[0].name" -o tsv)
DEP=$(az deployment group list --resource-group $RG --query "[0].name" -o tsv)

az deployment group show -g $RG -n $DEP --query properties.outputs -o json
```

Key resources provisioned:

- **Foundry AIServices account** (hosts Content Understanding + Azure OpenAI)
- **Foundry project**
- **`gpt-4.1`** chat deployment
- **`text-embedding-3-large`** embedding deployment (3072 dims)
- **Azure AI Search** service on **Basic** SKU (semantic ranker requires Basic)
- **Storage account** with empty `ai103-source` blob container

## Configure your environment

```bash
cp .env.example pipeline/.env
# fill in values from the ARM deployment outputs (see Exercise 1 Step 3)
```

Grant your signed-in UPN the data-plane roles you will need:

| Scope           | Role                                          |
|-----------------|-----------------------------------------------|
| Storage account | `Storage Blob Data Contributor`               |
| Search service  | `Search Service Contributor` + `Search Index Data Contributor` |
| Foundry account | `Cognitive Services OpenAI User` / `Azure AI User` |

Wait ~60 seconds after each `az role assignment create` for RBAC propagation.

## Install

```bash
python -m venv .venv
source .venv/bin/activate        # or: .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Run the pipeline (after completing Exercises 1-3)

```bash
# 1. Author the analyzer (Exercise 1)
python -c "from pipeline.cu_extract import ensure_analyzer; ensure_analyzer()"

# 2. Build the index (Exercise 3)
python -m pipeline.index

# 3. Upload the sample docs then run ingest (Exercise 2)
az storage blob upload-batch --account-name $STG --destination ai103-source \
    --source ./sample_data --auth-mode login
python -m pipeline.ingest

# 4. Query (Exercise 4)
python -m pipeline.query "What is the total of invoice INV-9001?"
python -m pipeline.query --cite "Which vendor had the highest invoice total?"
```

## Run the FastAPI app

```bash
uvicorn app.main:app --reload --port 8000
```

Then:

```bash
curl "http://localhost:8000/search?q=warranty%20coverage"
curl -X POST http://localhost:8000/chat \
     -H "Content-Type: application/json" \
     -d '{"question": "What does the Alpine Supply Co. contract cover?"}'
```

## Vector dimension contract

`text-embedding-3-large` emits 3072-dim vectors. The index field is
`vector_search_dimensions=3072`. Query vectors must be length 3072. If any
of those three values drift, uploads succeed but queries return zero hits.
Do **not** pass `dimensions=1536` to `embeddings.create`.
