"""
Hybrid Search Pipeline (BM25 + pgvector + RRF)
Course 202 - Lesson 6: Hybrid Search Pipeline

Exercise 1: BM25 + pgvector hybrid search with RRF (Reciprocal Rank Fusion)
Exercise 2: Cross-encoder re-ranker that improves top-k precision

BM25 captures exact keyword matches; vector search captures semantic similarity.
RRF combines the ranked lists from both methods into one superior ranking.

Uses the same documentation corpus as the pgvector lesson.
Database: postgresql://postgres:postgres@localhost:5432/embeddings_db

IMPORTANT: OPENAI_API_KEY and OPENAI_BASE_URL are pre-configured in your
environment automatically.
"""
from openai import OpenAI
import psycopg2
import numpy as np
from rank_bm25 import BM25Okapi
import re
import time

client = OpenAI()

DB_CONFIG = {
    "host": "localhost", "port": 5432,
    "dbname": "embeddings_db", "user": "postgres", "password": "postgres"
}

EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSIONS = 1536

# Same documentation corpus from pgvector lesson
CORPUS = [
    {"id": 1,  "source": "api-guide", "title": "Authentication",       "content": "The OpenAI API uses API keys for authentication. Include your key in the Authorization header as 'Bearer YOUR_API_KEY'. Never expose your API key in client-side code or commit it to version control."},
    {"id": 2,  "source": "api-guide", "title": "Rate Limits",           "content": "Rate limits are enforced per model and per organization. Requests that exceed limits receive a 429 HTTP response. Implement exponential backoff: wait 2^n seconds between retries, starting with n=1."},
    {"id": 3,  "source": "api-guide", "title": "Streaming",             "content": "Set stream=True to receive server-sent events (SSE). The response will be chunks with delta content. Use the text_stream iterator for simple text streaming or handle raw events for full control."},
    {"id": 4,  "source": "api-guide", "title": "Token Limits",          "content": "Each model has a maximum context window measured in tokens. GPT-4.1 supports up to 1 million tokens. Monitor usage via the response.usage object which contains input_tokens and output_tokens."},
    {"id": 5,  "source": "api-guide", "title": "Embeddings",            "content": "Use text-embedding-3-small for cost-effective embeddings or text-embedding-3-large for higher quality. Reduce dimensions with the dimensions parameter. Embeddings are normalized by default."},
    {"id": 6,  "source": "best-practices", "title": "Prompt Design",    "content": "Be specific and provide context. Use system prompts to set behavior. Chain prompts for complex tasks. Include examples in few-shot prompting. Avoid vague instructions."},
    {"id": 7,  "source": "best-practices", "title": "Cost Optimization","content": "Use gpt-4.1-mini for most tasks and reserve gpt-4.1 for complex reasoning. Cache repeated prompts. Use the Batch API for non-time-sensitive workloads at 50% cost."},
    {"id": 8,  "source": "best-practices", "title": "Error Handling",   "content": "Always handle APIError, RateLimitError, and APIConnectionError. Implement retry logic with backoff. Log all API calls with timestamps, model, and token counts."},
    {"id": 9,  "source": "responses-api", "title": "Tool Calling",      "content": "Define tools with JSON Schema. Set strict=True for guaranteed schema adherence. The model returns function_call items in output. Execute tools and feed results back."},
    {"id": 10, "source": "responses-api", "title": "Structured Output", "content": "Use response_format with json_schema for JSON output. Use client.responses.parse() with Pydantic models for typed output. Handle refusals when the model cannot comply."},
    {"id": 11, "source": "responses-api", "title": "File Search",       "content": "Create vector stores and upload files. Files are automatically chunked and embedded. Use the file_search tool to query documents. Manage vector store lifecycle with expiration policies."},
    {"id": 12, "source": "models", "title": "GPT-4.1",                  "content": "GPT-4.1 is the flagship model with 1M token context window. Best for complex analysis, code generation, and tasks requiring high accuracy. Costs $2.00/1M input tokens."},
    {"id": 13, "source": "models", "title": "GPT-4.1-mini",             "content": "GPT-4.1-mini balances capability and cost. Suitable for most production use cases including classification, extraction, and generation. Costs $0.40/1M input tokens."},
    {"id": 14, "source": "models", "title": "GPT-4.1-nano",             "content": "GPT-4.1-nano is the fastest and cheapest model. Best for classification, simple routing, and high-volume tasks. Costs $0.10/1M input tokens."},
    {"id": 15, "source": "models", "title": "Reasoning Models",         "content": "o3 and o4-mini use extended chain-of-thought reasoning for math, code, and complex logic. Control thinking depth with reasoning_effort: low, medium, or high."},
    {"id": 16, "source": "security", "title": "Prompt Injection",       "content": "Prompt injection attacks attempt to override your system prompt via user input. Defend with input validation, instruction separation, output validation, and limiting model permissions."},
    {"id": 17, "source": "security", "title": "Data Privacy",           "content": "Do not send personally identifiable information (PII) to the API unless necessary. Use the Moderation API to filter harmful content. Implement audit logging for compliance."},
    {"id": 18, "source": "security", "title": "API Key Management",     "content": "Rotate API keys regularly. Use environment variables or secret managers, never hardcode keys. Set IP allow lists in the OpenAI dashboard."},
    {"id": 19, "source": "fine-tuning", "title": "When to Fine-Tune",   "content": "Fine-tune when prompt engineering cannot achieve required accuracy, or when you need consistent formatting or tone. Not recommended for knowledge updates - use RAG instead."},
    {"id": 20, "source": "fine-tuning", "title": "Training Data",       "content": "Prepare data as JSONL with system, user, and assistant message structure. Aim for 50-100 high-quality examples minimum. Quality matters more than quantity."},
]


def tokenize(text: str) -> list[str]:
    """Simple tokenizer: lowercase, split on non-alphanumeric."""
    return re.findall(r'\w+', text.lower())


def get_embedding(text: str) -> list[float]:
    """Generate embedding using text-embedding-3-small."""
    response = client.embeddings.create(
        model=EMBEDDING_MODEL, input=text, dimensions=EMBEDDING_DIMENSIONS
    )
    return response.data[0].embedding


def bm25_search(query: str, corpus: list[dict], top_k: int = 20) -> list[tuple[int, float]]:
    """
    Exercise 1a: BM25 keyword search.

    1. Tokenize each document's title + content using tokenize()
    2. Build a BM25Okapi index from the tokenized corpus
    3. Tokenize the query and get BM25 scores using bm25.get_scores()
    4. Return top_k (doc_id, bm25_score) pairs sorted by score descending

    Args:
        query: Search query
        corpus: List of document dicts
        top_k: Number of results to return

    Returns:
        List of (doc_id, bm25_score) sorted by score descending
    """
    # Tokenize all documents
    tokenized_corpus = [tokenize(f"{doc['title']} {doc['content']}") for doc in corpus]

    # TODO: Build BM25Okapi(tokenized_corpus)
    # TODO: bm25.get_scores(tokenize(query)) to get scores array
    # TODO: Get top_k (id, score) pairs sorted by score descending
    # Return list of (corpus[i]["id"], score) tuples
    return []


def vector_search(query: str, corpus: list[dict], top_k: int = 20) -> list[tuple[int, float]]:
    """
    Exercise 1b: Vector similarity search using OpenAI embeddings.

    1. Generate query embedding
    2. Generate embeddings for all documents (title + content)
    3. Compute cosine similarity between query and each document
    4. Return top_k (doc_id, similarity_score) pairs

    Note: For production, embeddings would be pre-computed and stored in pgvector.
    Here we compute them on the fly for simplicity.

    Args:
        query: Search query
        corpus: List of document dicts
        top_k: Number of results to return

    Returns:
        List of (doc_id, similarity_score) sorted by similarity descending
    """
    query_emb = np.array(get_embedding(query))
    results = []

    print(f"  Computing {len(corpus)} embeddings for vector search...")
    for doc in corpus:
        text = f"{doc['title']}: {doc['content']}"
        doc_emb = np.array(get_embedding(text))
        # TODO: Compute cosine similarity = np.dot(query_emb, doc_emb) / (norm * norm)
        similarity = 0.0  # Replace with your calculation
        results.append((doc["id"], similarity))

    # TODO: Sort by similarity descending and return top_k
    return results[:top_k]


def reciprocal_rank_fusion(results_a: list[tuple[int, float]],
                           results_b: list[tuple[int, float]],
                           k: int = 60) -> list[tuple[int, float]]:
    """
    Exercise 1c: Combine two ranked lists using Reciprocal Rank Fusion (RRF).

    RRF formula: score(d) = sum(1 / (k + rank(d))) for each result list

    For each doc_id, compute its RRF score from both lists.
    Docs appearing in only one list still get a score from that list.

    Args:
        results_a: First ranked list (doc_id, score) - e.g., BM25 results
        results_b: Second ranked list (doc_id, score) - e.g., vector results
        k: Constant to prevent over-ranking top results (default: 60)

    Returns:
        Combined ranking sorted by RRF score descending
    """
    rrf_scores: dict[int, float] = {}

    # TODO: For each (doc_id, _) in results_a, with rank starting at 1:
    #   rrf_scores[doc_id] = rrf_scores.get(doc_id, 0) + 1 / (k + rank)

    # TODO: For each (doc_id, _) in results_b, with rank starting at 1:
    #   rrf_scores[doc_id] = rrf_scores.get(doc_id, 0) + 1 / (k + rank)

    # TODO: Sort rrf_scores by value descending and return as list of (doc_id, rrf_score)
    return sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)


def cross_encoder_rerank(query: str, candidates: list[dict], top_k: int = 5) -> list[dict]:
    """
    Exercise 2: Re-rank candidates using GPT-4.1-mini as a cross-encoder.

    Ask the model to score each candidate's relevance to the query (0-10).
    Use a single API call with all candidates listed.
    Return top_k candidates sorted by the model's relevance scores.

    The model should evaluate: does this document actually answer the query?

    Args:
        query: The search query
        candidates: Top-20 candidate documents to re-rank
        top_k: Final number of results

    Returns:
        Top-k candidates sorted by relevance (highest first)
    """
    if not candidates:
        return []

    # Build the re-ranking prompt
    docs_text = "\n".join([
        f"[{i}] {doc['title']}: {doc['content'][:100]}..."
        for i, doc in enumerate(candidates)
    ])

    prompt = f"""Query: "{query}"

Score each document's relevance to the query from 0 to 10.
0 = completely irrelevant, 10 = directly answers the query.

Documents:
{docs_text}

Return a JSON array of scores in order: [score_0, score_1, ...]"""

    # TODO: Call client.responses.create() with model="gpt-4.1-mini"
    # TODO: Parse the JSON array from response.output_text
    # TODO: Zip scores with candidates and sort by score descending
    # TODO: Return top_k candidates with score added
    return candidates[:top_k]


def hybrid_search(query: str, top_k: int = 5) -> list[dict]:
    """
    Exercise 1d: Full hybrid search pipeline.

    1. BM25 search (top 20)
    2. Vector search (top 20)
    3. RRF fusion
    4. Return top_k fused results with document details
    """
    print(f"\nHybrid search for: '{query}'")

    print("  Running BM25 search...")
    bm25_results = bm25_search(query, CORPUS, top_k=20)

    print("  Running vector search...")
    vector_results = vector_search(query, CORPUS, top_k=20)

    print("  Applying RRF fusion...")
    fused = reciprocal_rank_fusion(bm25_results, vector_results)

    # Look up full document details for top results
    doc_lookup = {doc["id"]: doc for doc in CORPUS}
    results = []
    for doc_id, rrf_score in fused[:top_k]:
        doc = doc_lookup.get(doc_id, {}).copy()
        doc["rrf_score"] = rrf_score
        results.append(doc)

    return results


if __name__ == "__main__":
    queries = [
        "how to handle API rate limiting",
        "authentication API key security",
        "reasoning models for complex tasks",
    ]

    print("=" * 60)
    print("Exercise 1: Hybrid Search (BM25 + Vector + RRF)")
    print("=" * 60)

    for query in queries:
        results = hybrid_search(query, top_k=5)
        print(f"\nResults for: '{query}'")
        for rank, doc in enumerate(results, 1):
            print(f"  {rank}. [{doc.get('rrf_score', 0):.4f}] {doc.get('title', 'N/A')}")

    print("\n" + "=" * 60)
    print("Exercise 2: Cross-Encoder Re-Ranking")
    print("=" * 60)

    query = "what model should I use for code generation?"
    # Get candidates from hybrid search
    candidates = hybrid_search(query, top_k=20)
    print(f"\nRe-ranking {len(candidates)} candidates for: '{query}'")
    reranked = cross_encoder_rerank(query, candidates, top_k=5)
    print("Re-ranked top 5:")
    for rank, doc in enumerate(reranked, 1):
        score = doc.get('relevance_score', 'N/A')
        print(f"  {rank}. [{score}] {doc.get('title', 'N/A')}")
