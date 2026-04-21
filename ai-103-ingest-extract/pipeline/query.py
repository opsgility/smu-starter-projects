"""Hybrid retrieval + grounded citations for the Summitline knowledge base.

Exercise 4 (Lab 2273 / 3409) ships the `query()` function fully implemented
so you can inspect the hybrid retrieval shape. You implement:

  * cite()         - grounded-answer helper that post-validates [markers]
  * CLI entrypoint - plain `python -m pipeline.query "..."` and `--cite`

Run without citations:
    python -m pipeline.query "What is the total of invoice INV-9001?"

Run with citations:
    python -m pipeline.query --cite "What is the total of invoice INV-9001?"
"""
from __future__ import annotations

import os
import re
import sys

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import (
    QueryAnswerType,
    QueryCaptionType,
    QueryType,
    VectorizedQuery,
)
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT_ENDPOINT = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
EMBED_DEPLOYMENT = os.environ["EMBEDDING_DEPLOYMENT"]
SEARCH_ENDPOINT = os.environ["AZURE_SEARCH_ENDPOINT"]
INDEX = os.environ["AZURE_SEARCH_INDEX"]

CRED = DefaultAzureCredential()

search_client = SearchClient(SEARCH_ENDPOINT, INDEX, CRED)


# ---------------------------------------------------------------------------
# Embedding helper
# ---------------------------------------------------------------------------

def _embed_one(text: str) -> list[float]:
    """Embed a single query string through the Foundry project's OpenAI client."""
    client = AIProjectClient(
        endpoint=PROJECT_ENDPOINT,
        credential=CRED,
    ).get_openai_client()
    resp = client.embeddings.create(model=EMBED_DEPLOYMENT, input=[text])
    return resp.data[0].embedding


# ---------------------------------------------------------------------------
# Hybrid retrieval
# ---------------------------------------------------------------------------

def query(text: str, k: int = 5) -> list[dict]:
    """Run a hybrid (BM25 + HNSW + semantic ranker) query over the index.

    Returns the top `k` hits as dicts with `id`, `source`, `doc_type`,
    `score` (BM25+vector fused), `rerank` (semantic reranker), and `snippet`.
    """
    qvec = _embed_one(text)
    results = search_client.search(
        search_text=text,
        vector_queries=[VectorizedQuery(vector=qvec,
                                        k_nearest_neighbors=50,
                                        fields="embedding")],
        query_type=QueryType.SEMANTIC,
        semantic_configuration_name="default",
        query_caption=QueryCaptionType.EXTRACTIVE,
        query_answer=QueryAnswerType.EXTRACTIVE,
        top=k,
    )

    hits = []
    for r in results:
        caption = ""
        caps = r.get("@search.captions", [])
        if caps:
            caption = caps[0].text
        hits.append({
            "id":       r["id"],
            "source":   r["source"],
            "doc_type": r.get("doc_type", ""),
            "score":    r.get("@search.score", 0),
            "rerank":   r.get("@search.rerankerScore", 0),
            "snippet":  caption or r["markdown"][:240],
        })
    return hits


# ---------------------------------------------------------------------------
# Grounded citation helper
# ---------------------------------------------------------------------------

_MARKER_RE = re.compile(r"\[([^\[\]]+?)\]")


def _extract_markers(text: str) -> list[str]:
    """Return the set of [bracket] markers the model emitted."""
    return sorted(set(_MARKER_RE.findall(text)))


def cite(question: str, k: int = 5) -> dict:
    """Produce a grounded answer with post-validated [source#chunkN] citations.

    Returns a dict with `answer`, `citations` (markers found in the answer),
    and `invalid_citations` (markers that do NOT match any retrieved hit).
    """
    # TODO (Exercise 4 Step 3): Implement the cite() helper.
    # 1. hits = query(question, k)
    # 2. Build a context string that joins each hit as
    #       "[{source}#chunk{id.rsplit('_',1)[-1]}] {snippet}"
    #    separated by blank lines.
    # 3. Build a strict system prompt that tells the model to answer ONLY
    #    from the context and cite [source#chunk] tags EXACTLY as shown.
    # 4. Use AIProjectClient(endpoint=AZURE_AI_PROJECT_ENDPOINT, credential=CRED)
    #    as a context manager, then `proj.get_openai_client()` similarly, and
    #    call client.responses.create(model=MODEL_DEPLOYMENT, temperature=0,
    #    input=[system, user]) where user = f"Context:\n{context}\n\nQ: {question}".
    # 5. answer = resp.output_text
    # 6. markers = _extract_markers(answer)
    # 7. valid_tags = {f"{h['source']}#chunk{h['id'].rsplit('_',1)[-1]}" for h in hits}
    # 8. invalid = [m for m in markers if m not in valid_tags]
    # 9. Return {"answer": ..., "citations": markers, "invalid_citations": invalid}.
    raise NotImplementedError("Implement cite() in Exercise 4 Step 3.")


# ---------------------------------------------------------------------------
# CLI entry-point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # TODO (Exercise 4 Step 4): Implement the CLI entry-point.
    # If sys.argv looks like:   --cite <question words...>
    #   - call cite(" ".join(sys.argv[2:]))
    #   - print result["answer"], then "citations: <list>"
    #   - if invalid_citations is non-empty, print a WARNING line with them.
    # Otherwise treat sys.argv[1:] as the question:
    #   - for each hit from query("..."), print:
    #       f"{h['score']:.3f}  rerank={h['rerank']:.2f}  {h['source']:30s} ({h['doc_type']})"
    #       f"   {h['snippet']}"
    raise NotImplementedError("Implement the CLI branch in Exercise 4 Step 4.")
