"""
Hybrid Search Pipeline
Course 202 - Lesson 6: Hybrid Search & Re-Ranking

Build a hybrid search pipeline combining BM25 keyword search with
vector search using Reciprocal Rank Fusion (RRF).

IMPORTANT: OPENAI_API_KEY and OPENAI_BASE_URL are pre-configured in your
environment automatically. Do NOT set them manually.
"""
from openai import OpenAI
from rank_bm25 import BM25Okapi
import numpy as np
import json

client = OpenAI()

# Documentation corpus for search
CORPUS = [
    {"id": 1, "title": "Python Installation", "content": "Install Python 3.11 from python.org. Use pyenv for version management. Run python --version to verify. pip is included with Python 3.4+."},
    {"id": 2, "title": "Virtual Environments", "content": "Create virtual environments with python -m venv myenv. Activate with source myenv/bin/activate on Linux or myenv\\Scripts\\activate on Windows. Install packages with pip."},
    {"id": 3, "title": "pip Package Manager", "content": "pip install package-name installs packages. pip install -r requirements.txt installs from file. pip list shows installed packages. pip freeze > requirements.txt exports dependencies."},
    {"id": 4, "title": "Type Annotations", "content": "Python 3.5+ supports type hints: def greet(name: str) -> str. Use Optional[str] for nullable fields. The mypy tool checks types statically without running code."},
    {"id": 5, "title": "Async Programming", "content": "Use async def for coroutines and await for async calls. asyncio.run() starts the event loop. aiohttp enables async HTTP requests. async with opens async context managers."},
    {"id": 6, "title": "List Comprehensions", "content": "List comprehensions: [x*2 for x in range(10)]. Filter with condition: [x for x in items if x > 0]. Nested: [f(x,y) for x in xs for y in ys]."},
    {"id": 7, "title": "Error Handling", "content": "Use try/except to catch exceptions. except ValueError as e captures the error. finally runs cleanup code. raise re-raises or raises new exceptions. Custom exceptions extend Exception."},
    {"id": 8, "title": "Dataclasses", "content": "from dataclasses import dataclass. @dataclass decorator auto-generates __init__, __repr__, __eq__. Use field(default_factory=list) for mutable defaults. frozen=True makes instances immutable."},
    {"id": 9, "title": "Context Managers", "content": "The with statement manages resources. with open('file') as f automatically closes the file. Implement __enter__ and __exit__ or use @contextmanager decorator."},
    {"id": 10, "title": "Generators", "content": "Generators use yield instead of return. They are memory-efficient for large sequences. Generator expressions: (x*2 for x in range(1000)). Use next() to advance manually."},
]


def get_embedding(text: str) -> list[float]:
    """Get embedding for a text using text-embedding-3-small."""
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )
    return response.data[0].embedding


def cosine_similarity(v1: list[float], v2: list[float]) -> float:
    a, b = np.array(v1), np.array(v2)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def build_bm25_index(corpus: list[dict]) -> BM25Okapi:
    """Build a BM25 index from the corpus title + content."""
    tokenized = [(doc["title"] + " " + doc["content"]).lower().split() for doc in corpus]
    return BM25Okapi(tokenized)


def bm25_search(query: str, bm25: BM25Okapi, corpus: list[dict], top_k: int = 10) -> list[tuple]:
    """
    Exercise 1: Perform BM25 keyword search.

    Tokenize the query (lowercase split), compute BM25 scores,
    return top_k results as [(doc_id, score), ...] sorted descending.
    """
    # TODO: Tokenize query: query.lower().split()
    # TODO: scores = bm25.get_scores(tokenized_query)
    # TODO: Get top_k indices: np.argsort(scores)[::-1][:top_k]
    # TODO: Return [(corpus[i]["id"], scores[i]) for i in top_k_indices]
    pass


def vector_search(query_embedding: list[float], corpus: list[dict],
                   embeddings: list[list[float]], top_k: int = 10) -> list[tuple]:
    """
    Exercise 2: Perform vector similarity search.

    Compute cosine similarity between query and all document embeddings.
    Return top_k results as [(doc_id, score), ...] sorted descending.
    """
    # TODO: Compute cosine_similarity(query_embedding, emb) for each emb in embeddings
    # TODO: Sort by score descending, return top_k as [(doc_id, score), ...]
    pass


def reciprocal_rank_fusion(bm25_results: list[tuple], vector_results: list[tuple],
                            k: int = 60) -> list[tuple]:
    """
    Exercise 3: Combine BM25 and vector results using Reciprocal Rank Fusion.

    RRF score for a document = sum(1 / (k + rank)) across all result lists.
    where rank is the 1-based position in each ranked list.

    Returns combined results as [(doc_id, rrf_score), ...] sorted descending.
    """
    rrf_scores = {}

    # TODO: For each list (bm25_results, vector_results):
    #   for rank, (doc_id, _) in enumerate(results, start=1):
    #       rrf_scores[doc_id] = rrf_scores.get(doc_id, 0) + 1 / (k + rank)
    # TODO: Sort by rrf_score descending
    # TODO: Return [(doc_id, score), ...]
    pass


def hybrid_search(query: str, corpus: list[dict], embeddings: list[list[float]],
                   bm25: BM25Okapi, top_k: int = 5) -> list[dict]:
    """
    Exercise 4: Run the full hybrid search pipeline.

    Steps:
    1. Embed the query
    2. Run bm25_search() and vector_search()
    3. Fuse with reciprocal_rank_fusion()
    4. Return top_k documents from corpus with their RRF scores
    """
    # TODO: get_embedding(query)
    # TODO: Run both searches with top_k=10
    # TODO: Fuse results with RRF
    # TODO: Look up docs by id, return top_k results with score
    pass


if __name__ == "__main__":
    print("Hybrid Search Pipeline — Course 202 Lesson 6")
    print("=" * 48)

    # Pre-compute embeddings for corpus
    print("Embedding corpus...")
    corpus_embeddings = [
        get_embedding(doc["title"] + " " + doc["content"])
        for doc in CORPUS
    ]

    # Build BM25 index
    bm25 = build_bm25_index(CORPUS)

    queries = [
        "install Python packages",
        "handle errors in Python",
        "async await programming",
    ]

    for query in queries:
        print(f"\nQuery: '{query}'")
        results = hybrid_search(query, CORPUS, corpus_embeddings, bm25, top_k=3)
        if results:
            for i, r in enumerate(results, 1):
                print(f"  {i}. [{r['score']:.4f}] {r['title']}")
