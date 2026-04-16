"""
Capstone Project: Enterprise RAG Assistant
Course 202 - Lesson 10: Capstone Project

Build a hybrid RAG assistant with:
1. Hybrid retrieval: BM25 + vector embeddings with RRF fusion
2. Cross-encoder re-ranking on top-20 candidates
3. Source attribution: every answer includes document source and title
4. Hallucination guard: verify answer is grounded in retrieved context
5. Evaluation report: precision@5, recall@5, hallucination rate across test queries

Uses the same documentation corpus defined in this file.

IMPORTANT: OPENAI_API_KEY and OPENAI_BASE_URL are pre-configured in your
environment automatically.
"""
from openai import OpenAI
from pydantic import BaseModel
from typing import Optional
import numpy as np
from rank_bm25 import BM25Okapi
import re
import json
from datetime import datetime, timezone

client = OpenAI()

# -----------------------------------------------------------------------
# Documentation corpus
# -----------------------------------------------------------------------
CORPUS = [
    {"id": 1,  "source": "authentication", "content": "API keys are used for authentication. Set OPENAI_API_KEY environment variable. Rotate keys regularly. Use project-scoped keys for security. Never expose keys in client-side code."},
    {"id": 2,  "source": "rate-limits",    "content": "Rate limits: 500 RPM default (Tier 1). 429 error = rate limited. Use exponential backoff with jitter. Batch API for non-urgent workloads at 50% cost reduction."},
    {"id": 3,  "source": "streaming",      "content": "Use client.responses.stream() for streaming. Iterate text_stream for text deltas. stream.get_final_response() for usage stats. Streaming improves perceived latency for users."},
    {"id": 4,  "source": "models",         "content": "GPT-4.1: $2.00/1M input, 1M context, best quality. GPT-4.1-mini: $0.40/1M input, balanced cost. GPT-4.1-nano: $0.10/1M input, fastest and cheapest for classification."},
    {"id": 5,  "source": "reasoning",      "content": "o3 and o4-mini are reasoning models with extended chain-of-thought. Use reasoning_effort: low/medium/high. Best for math, code debugging, complex logic. Do not prompt step-by-step."},
    {"id": 6,  "source": "embeddings",     "content": "text-embedding-3-small: 1536 dims, $0.02/1M tokens. text-embedding-3-large: 3072 dims, higher quality. Reduce dimensions for cost. Use cosine similarity for retrieval."},
    {"id": 7,  "source": "tool-calling",   "content": "Define tools with JSON Schema. strict=True guarantees schema adherence. tool_choice: auto, required, or none. Handle parallel tool calls by mapping results to tool_call_id."},
    {"id": 8,  "source": "structured-out", "content": "client.responses.parse() with Pydantic model for typed output. response_format json_object for untyped JSON. strict=True: all fields required, no additionalProperties. Handle refusals."},
    {"id": 9,  "source": "file-search",    "content": "Create vector stores with client.vector_stores.create(). Upload files with upload_and_poll(). Use file_search built-in tool in responses.create(). Manage expiration policies."},
    {"id": 10, "source": "fine-tuning",    "content": "SFT uses JSONL with system/user/assistant messages. DPO uses chosen/rejected pairs. RFT uses reward function scoring. Fine-tune for consistent format, style, and domain vocabulary."},
    {"id": 11, "source": "prompt-eng",     "content": "System prompts set role and behavior. Few-shot examples guide model output. Chain-of-thought improves accuracy for multi-step problems. Meta-prompting improves prompts iteratively."},
    {"id": 12, "source": "cost-opt",       "content": "Use GPT-4.1-nano for classification and routing. Cache semantic duplicates with Redis. Batch API saves 50% on non-urgent jobs. Track costs per user with cost attribution middleware."},
    {"id": 13, "source": "safety",         "content": "omni-moderation-latest screens text and images. Use dual moderation: check input AND output. 13 harm categories. Prompt injection defense: validate input, separate instructions, validate output."},
    {"id": 14, "source": "responses-api",  "content": "client.responses.create() is the modern API. previous_response_id for multi-turn state. Built-in tools: web_search, file_search, code_interpreter. MCP servers as native tool type."},
    {"id": 15, "source": "evals",          "content": "Evaluation types: exact match, semantic similarity, LLM-as-judge. Build golden datasets before prompts. Run evals in CI/CD to catch regressions. Use GPT-4.1 as judge with rubric."},
]

# Ground-truth answers for evaluation (source document IDs that should appear)
TEST_QUERIES = [
    {"query": "How do I handle 429 rate limit errors?",           "relevant_ids": [2]},
    {"query": "What model should I use for math problems?",        "relevant_ids": [5]},
    {"query": "How do embeddings work and which model is best?",   "relevant_ids": [6]},
    {"query": "How do I get typed Pydantic output from the API?",  "relevant_ids": [8]},
    {"query": "How do I authenticate with the OpenAI API?",        "relevant_ids": [1]},
]


# -----------------------------------------------------------------------
# Retrieval components (implement these)
# -----------------------------------------------------------------------

def tokenize(text: str) -> list[str]:
    return re.findall(r'\w+', text.lower())


def get_embedding(text: str) -> list[float]:
    """Generate embedding using text-embedding-3-small."""
    r = client.embeddings.create(model="text-embedding-3-small", input=text, dimensions=1536)
    return r.data[0].embedding


def bm25_search(query: str, top_k: int = 20) -> list[tuple[int, float]]:
    """
    Exercise 1a: BM25 keyword search over CORPUS.
    Return list of (doc_id, score) sorted by score descending.
    """
    tokenized = [tokenize(f"{doc['source']} {doc['content']}") for doc in CORPUS]
    # TODO: Build BM25Okapi(tokenized)
    # TODO: Get scores for tokenize(query)
    # TODO: Return top_k (CORPUS[i]["id"], score) pairs sorted descending
    return []


def vector_search(query: str, top_k: int = 20) -> list[tuple[int, float]]:
    """
    Exercise 1b: Vector similarity search over CORPUS.
    Return list of (doc_id, cosine_similarity) sorted descending.
    """
    query_emb = np.array(get_embedding(query))
    results = []
    for doc in CORPUS:
        doc_emb = np.array(get_embedding(doc['content']))
        # TODO: Compute cosine similarity
        similarity = float(np.dot(query_emb, doc_emb) /
                           (np.linalg.norm(query_emb) * np.linalg.norm(doc_emb)))
        results.append((doc["id"], similarity))
    return sorted(results, key=lambda x: x[1], reverse=True)[:top_k]


def rrf_fusion(bm25_results: list, vector_results: list, k: int = 60) -> list[tuple[int, float]]:
    """
    Exercise 1c: Reciprocal Rank Fusion.
    Combine two ranked lists, return (doc_id, rrf_score) sorted descending.
    """
    scores: dict[int, float] = {}
    for rank, (doc_id, _) in enumerate(bm25_results, 1):
        scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank)
    for rank, (doc_id, _) in enumerate(vector_results, 1):
        scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


def cross_encoder_rerank(query: str, candidates: list[dict], top_k: int = 5) -> list[dict]:
    """
    Exercise 2: Re-rank candidates with GPT-4.1-mini. Return top_k.
    """
    if not candidates:
        return []
    docs_text = "\n".join([f"[{i}] (source={d['source']}) {d['content'][:100]}"
                            for i, d in enumerate(candidates)])
    prompt = f"""Query: "{query}"
Score each document 0-10 for relevance. Return JSON array of scores: [score_0, score_1, ...]
Documents:
{docs_text}"""

    # TODO: Call client.responses.create(model="gpt-4.1-mini", input=prompt)
    # TODO: Parse JSON array from response.output_text
    # TODO: Sort candidates by score and return top_k with score added
    return candidates[:top_k]


# -----------------------------------------------------------------------
# Generation with source attribution
# -----------------------------------------------------------------------

class AnswerWithSources(BaseModel):
    answer: str
    sources: list[str]   # List of source document IDs cited
    confidence: float    # 0.0 to 1.0


class HallucinationCheck(BaseModel):
    is_grounded: bool
    ungrounded_claims: list[str]
    confidence: float


def generate_answer_with_attribution(query: str,
                                      context_docs: list[dict]) -> AnswerWithSources:
    """
    Exercise 3: Generate answer with mandatory source attribution.

    System prompt: "You are a technical documentation assistant. Answer ONLY
    based on the provided context. Always cite the source IDs you used."

    User prompt: includes query + context documents (with source IDs).

    Use client.responses.parse() with AnswerWithSources.

    Args:
        query: User question
        context_docs: Retrieved documents with source IDs

    Returns:
        AnswerWithSources with answer text and cited source IDs
    """
    system = """You are a technical documentation assistant. Answer ONLY based on the
provided context documents. Always cite which source IDs you used in your answer."""

    context_text = "\n\n".join([
        f"[Source: {doc['source']}]\n{doc['content']}"
        for doc in context_docs
    ])
    user = f"""Context documents:
{context_text}

Question: {query}

Answer the question using ONLY the context above. Cite the source IDs you used."""

    # TODO: Call client.responses.parse() with:
    #   model = "gpt-4.1-mini"
    #   input = [system message + user message]
    #   text_format = AnswerWithSources
    # TODO: Return response.output_parsed
    pass


def hallucination_guard(answer: str, context_docs: list[dict]) -> HallucinationCheck:
    """
    Exercise 4: Verify answer is grounded in retrieved context.

    Ask GPT-4.1 to check if the answer contains claims NOT supported
    by the context documents. Return HallucinationCheck.

    A claim is "ungrounded" if it cannot be traced to any context document.
    """
    context_text = "\n".join([f"[{doc['source']}] {doc['content']}" for doc in context_docs])
    prompt = f"""You are a fact-checker. Check if this answer is fully supported by the context.

Context:
{context_text}

Answer to check:
{answer}

Is every claim in the answer supported by the context?
List any claims NOT found in the context as ungrounded_claims."""

    # TODO: Call client.responses.parse() with model="gpt-4.1", text_format=HallucinationCheck
    # TODO: Return response.output_parsed
    pass


def full_rag_pipeline(query: str) -> dict:
    """
    Complete RAG pipeline: retrieve -> rerank -> generate -> guard.
    Returns dict with answer, sources, grounded status.
    """
    print(f"\nQuery: {query}")

    # Hybrid retrieval
    bm25_results = bm25_search(query, top_k=20)
    vector_results = vector_search(query, top_k=20)
    fused = rrf_fusion(bm25_results, vector_results)

    # Get top-20 candidate documents
    doc_lookup = {doc["id"]: doc for doc in CORPUS}
    candidates = [doc_lookup[doc_id] for doc_id, _ in fused[:20] if doc_id in doc_lookup]

    # Re-rank top-20 to get top-5
    top5 = cross_encoder_rerank(query, candidates, top_k=5)

    # Generate answer with attribution
    answer_obj = generate_answer_with_attribution(query, top5)

    # Hallucination guard
    guard_result = hallucination_guard(
        answer_obj.answer if answer_obj else "", top5
    )

    return {
        "query": query,
        "answer": answer_obj.answer if answer_obj else "",
        "sources": answer_obj.sources if answer_obj else [],
        "grounded": guard_result.is_grounded if guard_result else False,
        "ungrounded_claims": guard_result.ungrounded_claims if guard_result else [],
    }


def run_evaluation() -> None:
    """
    Exercise 5: Evaluate the RAG system.

    Run all TEST_QUERIES and compute:
    - Precision@5: of top-5 retrieved, how many are relevant?
    - Recall@5: of all relevant docs, how many appear in top-5?
    - Hallucination rate: % of answers flagged as ungrounded
    """
    print("\nRunning RAG evaluation...")
    results = []

    for test_case in TEST_QUERIES:
        result = full_rag_pipeline(test_case["query"])
        results.append(result)

    # Print evaluation report
    total = len(results)
    hallucinated = sum(1 for r in results if not r.get("grounded", True))
    hallucination_rate = hallucinated / total if total > 0 else 0

    print("\n" + "=" * 60)
    print("EVALUATION REPORT")
    print("=" * 60)
    print(f"Total queries evaluated: {total}")
    print(f"Hallucination rate: {hallucination_rate:.1%} {'✓ PASS' if hallucination_rate < 0.05 else '✗ FAIL'} (target < 5%)")
    print("\nPer-query results:")
    for i, r in enumerate(results):
        ground_status = "✓ Grounded" if r.get("grounded") else "✗ Hallucinated"
        print(f"  {i+1}. {ground_status} | Sources: {r.get('sources', [])}")
        print(f"     Answer: {r.get('answer', '')[:80]}...")


if __name__ == "__main__":
    print("Enterprise RAG Assistant - Capstone")
    print("=" * 60)

    # Demo single query
    demo_result = full_rag_pipeline("How do I save money on API costs?")
    print(f"\nAnswer: {demo_result['answer']}")
    print(f"Sources: {demo_result['sources']}")
    print(f"Grounded: {demo_result['grounded']}")

    # Full evaluation
    run_evaluation()
