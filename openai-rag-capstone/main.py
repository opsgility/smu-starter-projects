"""
Capstone Project: Enterprise RAG Assistant
Course 202 - Lesson 10: Capstone Project

Build a hybrid RAG assistant with:
1. Hybrid retrieval: in-memory vector search + BM25 with RRF fusion
2. Source attribution: every answer cites document and chunk
3. Hallucination guard: second LLM call verifies answer is grounded
4. Evaluation: precision@3 across test queries

IMPORTANT: OPENAI_API_KEY and OPENAI_BASE_URL are pre-configured in your
environment automatically. Do NOT set them manually.
"""
from openai import OpenAI
from pydantic import BaseModel
from rank_bm25 import BM25Okapi
import numpy as np
import json

client = OpenAI()

# Knowledge base
KNOWLEDGE_BASE = [
    {"id": 1, "source": "security-guide", "chunk": "Always use HTTPS for API communication. Store API keys in environment variables using os.getenv(), never hardcode them in source code. Rotate API keys every 90 days and audit access logs monthly."},
    {"id": 2, "source": "security-guide", "chunk": "Rate limiting protects APIs from abuse. Implement per-user limits (e.g., 100 req/min) and global limits. Return HTTP 429 with Retry-After header when limits are exceeded. Use token bucket or sliding window algorithms."},
    {"id": 3, "source": "security-guide", "chunk": "Input validation must happen at the API boundary. Validate JSON schema, string lengths, and data types. Sanitize strings against injection patterns. Never trust user-supplied data, even from authenticated users."},
    {"id": 4, "source": "performance-guide", "chunk": "Database connection pooling reduces latency by reusing connections. Use PgBouncer for PostgreSQL. Set pool_size=10 for small apps, up to CPU*2+1 for I/O bound apps. Monitor with pg_stat_activity."},
    {"id": 5, "source": "performance-guide", "chunk": "Redis caching dramatically reduces database load. Cache expensive query results with a TTL of 5-15 minutes. Use cache-aside pattern: check cache first, then database on miss, write to cache on hit. Monitor hit rate."},
    {"id": 6, "source": "performance-guide", "chunk": "Async programming with asyncio improves throughput for I/O-bound workloads. Use async def and await for network calls. aiohttp for async HTTP. asyncpg for async PostgreSQL. Benchmark with locust or k6."},
    {"id": 7, "source": "architecture-guide", "chunk": "Microservices communicate via REST APIs or message queues. Use REST for synchronous request-response. Use queues (RabbitMQ, Kafka) for async event-driven workflows. Document APIs with OpenAPI/Swagger."},
    {"id": 8, "source": "architecture-guide", "chunk": "The 12-factor app methodology: store config in environment variables, treat logs as event streams, run stateless processes, and declare dependencies explicitly in requirements files."},
    {"id": 9, "source": "testing-guide", "chunk": "Test pyramid: many unit tests, fewer integration tests, few end-to-end tests. Use pytest for Python. Mock external services with unittest.mock or pytest-mock. Aim for 80%+ code coverage on critical paths."},
    {"id": 10, "source": "testing-guide", "chunk": "Integration tests should use real databases and services when possible. Use Docker Compose to spin up test dependencies. Avoid testing against production. Use fixtures for test data setup and teardown."},
]

TEST_QUERIES = [
    {"query": "How should I store API keys?", "relevant_ids": [1]},
    {"query": "How do I improve database performance?", "relevant_ids": [4, 5]},
    {"query": "What is the best way to test my code?", "relevant_ids": [9, 10]},
]


class GroundednessCheck(BaseModel):
    is_grounded: bool
    confidence: float
    explanation: str


def get_embedding(text: str) -> list[float]:
    """Get embedding using text-embedding-3-small."""
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding


def cosine_similarity(v1: list[float], v2: list[float]) -> float:
    a, b = np.array(v1), np.array(v2)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def hybrid_retrieve(query: str, kb: list[dict], kb_embeddings: list[list[float]],
                     bm25: BM25Okapi, top_k: int = 3) -> list[dict]:
    """
    Exercise 1: Retrieve top_k chunks using hybrid BM25 + vector RRF.

    Steps:
    1. Embed the query
    2. BM25 search: bm25.get_scores(query.lower().split()) -> rank
    3. Vector search: cosine_similarity for each chunk -> rank
    4. RRF fusion: score += 1/(60 + rank) for each list
    5. Return top_k chunks sorted by RRF score, each with "rrf_score" field
    """
    # TODO: Implement hybrid retrieval with RRF (k=60)
    # TODO: Return top_k items from kb with added "rrf_score" field
    pass


def generate_answer(query: str, context_chunks: list[dict]) -> str:
    """
    Exercise 2: Generate a grounded answer with source attribution.

    Build a context string from the retrieved chunks, each prefixed with
    its source: "[security-guide] chunk text..."

    Use client.responses.create() with:
    - model="gpt-4.1-mini"
    - System: "Answer using only the provided context. Cite sources."
    - User: context + question

    Returns the answer text.
    """
    context = "\n\n".join(
        f"[{chunk['source']}] {chunk['chunk']}"
        for chunk in context_chunks
    )

    system = "Answer the question using only the provided context. Cite the source document name in brackets for each claim."
    user = f"Context:\n{context}\n\nQuestion: {query}"

    # TODO: Call client.responses.create() with system + user messages
    # TODO: Return response.output_text
    pass


def check_groundedness(answer: str, context_chunks: list[dict]) -> GroundednessCheck:
    """
    Exercise 3: Verify the answer is grounded in the retrieved context.

    Use client.responses.parse() with GroundednessCheck schema.
    Prompt: "Does this answer contain only information present in the context?
    Rate confidence 0.0-1.0."

    Returns GroundednessCheck with is_grounded, confidence, explanation.
    """
    context = "\n".join(chunk["chunk"] for chunk in context_chunks)

    system = "You are a fact-checker. Determine if the answer is fully grounded in the provided context."
    user = f"Context:\n{context}\n\nAnswer to verify:\n{answer}\n\nIs this answer grounded in the context? Rate confidence 0-1."

    # TODO: Call client.responses.parse() with GroundednessCheck schema
    # TODO: Return response.output_parsed (or a default if None)
    pass


def evaluate_retrieval(kb: list[dict], kb_embeddings: list[list[float]],
                        bm25: BM25Okapi) -> dict:
    """
    Exercise 4: Compute precision@3 across the TEST_QUERIES.

    precision@k = (relevant docs in top-k) / k

    For each test query:
    1. Run hybrid_retrieve(query, kb, kb_embeddings, bm25, top_k=3)
    2. Check which retrieved IDs are in the query's relevant_ids
    3. precision@3 = matches / 3

    Returns {"precision_at_3": float, "per_query": list}
    """
    # TODO: For each test query, retrieve top 3, compute precision@3
    # TODO: Return average precision@3 and per-query breakdown
    pass


if __name__ == "__main__":
    print("Enterprise RAG Assistant — Course 202 Capstone")
    print("=" * 50)

    # Pre-compute embeddings and BM25 index
    print("Building knowledge base index...")
    kb_texts = [f"{doc['source']}: {doc['chunk']}" for doc in KNOWLEDGE_BASE]
    kb_embeddings = [get_embedding(t) for t in kb_texts]
    bm25 = BM25Okapi([t.lower().split() for t in kb_texts])
    print(f"Indexed {len(KNOWLEDGE_BASE)} chunks.")

    # Run RAG pipeline on test queries
    for item in TEST_QUERIES:
        query = item["query"]
        print(f"\nQuery: {query}")

        chunks = hybrid_retrieve(query, KNOWLEDGE_BASE, kb_embeddings, bm25)
        if not chunks:
            continue

        answer = generate_answer(query, chunks)
        if answer:
            print(f"Answer: {answer[:300]}")

        check = check_groundedness(answer, chunks) if answer else None
        if check:
            status = "GROUNDED" if check.is_grounded else "HALLUCINATION DETECTED"
            print(f"Groundedness: {status} ({check.confidence:.0%}) — {check.explanation}")

    # Evaluate retrieval quality
    print("\n--- Retrieval Evaluation ---")
    eval_results = evaluate_retrieval(KNOWLEDGE_BASE, kb_embeddings, bm25)
    if eval_results:
        print(f"Precision@3: {eval_results['precision_at_3']:.2%}")
        for q in eval_results.get("per_query", []):
            print(f"  {q['query'][:50]}: {q['precision']:.2%}")
