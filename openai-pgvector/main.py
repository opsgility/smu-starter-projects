"""
Persistent Embedding Store with pgvector
Course 202 - Lesson 4: Persistent Embedding Store

Exercises:
1. Connect to PostgreSQL with psycopg2 and enable the pgvector extension
2. Create an embeddings table with a vector(1536) column and HNSW index
3. Chunk a documentation corpus and store embeddings in pgvector
4. Retrieve semantically similar chunks using the <=> cosine distance operator

Database connection: PostgreSQL runs locally in this lab environment.
Connection string: postgresql://postgres:postgres@localhost:5432/embeddings_db

IMPORTANT: OPENAI_API_KEY and OPENAI_BASE_URL are pre-configured in your
environment automatically.
"""
from openai import OpenAI
import psycopg2
from psycopg2.extras import execute_values
import numpy as np
import json
import time

client = OpenAI()

# Database connection configuration
DB_CONFIG = {
    "host":     "localhost",
    "port":     5432,
    "dbname":   "embeddings_db",
    "user":     "postgres",
    "password": "postgres"
}

EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSIONS = 1536

# Sample documentation corpus to embed (chunks of text)
DOCUMENTATION_CORPUS = [
    {"source": "api-guide", "title": "Authentication", "content": "The OpenAI API uses API keys for authentication. Include your key in the Authorization header as 'Bearer YOUR_API_KEY'. Never expose your API key in client-side code or commit it to version control."},
    {"source": "api-guide", "title": "Rate Limits", "content": "Rate limits are enforced per model and per organization. Requests that exceed limits receive a 429 HTTP response. Implement exponential backoff: wait 2^n seconds between retries, starting with n=1."},
    {"source": "api-guide", "title": "Streaming", "content": "Set stream=True to receive server-sent events (SSE). The response will be chunks with delta content. Use the text_stream iterator for simple text streaming or handle raw events for full control."},
    {"source": "api-guide", "title": "Token Limits", "content": "Each model has a maximum context window measured in tokens. GPT-4.1 supports up to 1 million tokens. Monitor usage via the response.usage object which contains input_tokens and output_tokens."},
    {"source": "api-guide", "title": "Embeddings", "content": "Use text-embedding-3-small for cost-effective embeddings or text-embedding-3-large for higher quality. Reduce dimensions with the dimensions parameter. Embeddings are normalized by default, enabling dot product as a similarity measure."},
    {"source": "best-practices", "title": "Prompt Design", "content": "Be specific and provide context. Use system prompts to set behavior. Chain prompts for complex tasks. Include examples in few-shot prompting. Avoid vague instructions that could be interpreted multiple ways."},
    {"source": "best-practices", "title": "Cost Optimization", "content": "Use gpt-4.1-mini for most tasks and reserve gpt-4.1 for complex reasoning. Cache repeated prompts. Use the Batch API for non-time-sensitive workloads at 50% cost. Monitor spend with the usage dashboard."},
    {"source": "best-practices", "title": "Error Handling", "content": "Always handle APIError, RateLimitError, and APIConnectionError. Implement retry logic with backoff. Log all API calls with timestamps, model, and token counts for debugging and cost tracking."},
    {"source": "responses-api", "title": "Tool Calling", "content": "Define tools with JSON Schema. Set strict=True for guaranteed schema adherence. The model returns function_call items in output. Execute tools and feed results back using function_call_output. Support parallel tool calls."},
    {"source": "responses-api", "title": "Structured Output", "content": "Use response_format with json_schema for JSON output. Use client.responses.parse() with Pydantic models for typed output. Strict mode requires all fields to have no additionalProperties. Handle refusals when the model cannot comply."},
    {"source": "responses-api", "title": "File Search", "content": "Create vector stores and upload files. Files are automatically chunked and embedded. Use the file_search tool in responses.create() to query your documents. Manage vector store lifecycle with expiration policies."},
    {"source": "models", "title": "GPT-4.1", "content": "GPT-4.1 is the flagship model with 1M token context window. Best for complex analysis, code generation, and tasks requiring high accuracy. Costs $2.00/1M input tokens and $8.00/1M output tokens."},
    {"source": "models", "title": "GPT-4.1-mini", "content": "GPT-4.1-mini balances capability and cost. Suitable for most production use cases including classification, extraction, and generation. Costs $0.40/1M input tokens and $1.60/1M output tokens."},
    {"source": "models", "title": "GPT-4.1-nano", "content": "GPT-4.1-nano is the fastest and cheapest model. Best for classification, simple routing, and high-volume tasks. Costs $0.10/1M input tokens and $0.40/1M output tokens."},
    {"source": "models", "title": "Reasoning Models", "content": "o3 and o4-mini use extended chain-of-thought reasoning for math, code, and complex logic. Control thinking depth with reasoning_effort: low, medium, or high. Do not instruct these models to 'think step by step' - they do it internally."},
    {"source": "security", "title": "Prompt Injection", "content": "Prompt injection attacks attempt to override your system prompt via user input. Defend with: input validation, instruction separation, output validation, and limiting model permissions. Never trust user input directly in system prompts."},
    {"source": "security", "title": "Data Privacy", "content": "Do not send personally identifiable information (PII) to the API unless necessary. Use the Moderation API to filter harmful content. Implement audit logging for compliance. Review OpenAI's data usage policies for enterprise customers."},
    {"source": "security", "title": "API Key Management", "content": "Rotate API keys regularly. Use environment variables or secret managers, never hardcode keys. Set IP allow lists in the OpenAI dashboard. Use project-level keys for scoped access to specific models."},
    {"source": "fine-tuning", "title": "When to Fine-Tune", "content": "Fine-tune when prompt engineering cannot achieve required accuracy, when you need consistent formatting or tone, or when reducing prompt token usage is a priority. Not recommended for knowledge updates - use RAG instead."},
    {"source": "fine-tuning", "title": "Training Data", "content": "Prepare data as JSONL with system, user, and assistant message structure. Aim for 50-100 high-quality examples minimum. Diversity and quality matter more than quantity. Validate format with the OpenAI file validation endpoint before submitting."},
]


def get_embedding(text: str) -> list[float]:
    """Generate embedding using text-embedding-3-small."""
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text,
        dimensions=EMBEDDING_DIMENSIONS
    )
    return response.data[0].embedding


def connect_db():
    """Connect to PostgreSQL and return connection."""
    return psycopg2.connect(**DB_CONFIG)


def setup_database(conn) -> None:
    """
    Exercise 1: Set up the pgvector database.

    Execute these SQL statements in order:
    1. CREATE EXTENSION IF NOT EXISTS vector;
    2. DROP TABLE IF EXISTS embeddings CASCADE;
    3. CREATE TABLE embeddings (
           id SERIAL PRIMARY KEY,
           source TEXT,
           title TEXT,
           content TEXT,
           embedding vector(1536)
       );

    Commit after creating the table.

    Args:
        conn: psycopg2 connection object
    """
    with conn.cursor() as cur:
        # TODO: Execute "CREATE EXTENSION IF NOT EXISTS vector;"
        # TODO: Execute "DROP TABLE IF EXISTS embeddings CASCADE;"
        # TODO: Execute the CREATE TABLE statement above
        # TODO: conn.commit()
        pass


def create_hnsw_index(conn) -> None:
    """
    Exercise 2: Create an HNSW index for fast nearest-neighbor search.

    HNSW (Hierarchical Navigable Small World) is the recommended index for
    pgvector. It offers excellent query performance for high-dimensional vectors.

    SQL: CREATE INDEX IF NOT EXISTS embeddings_hnsw_idx
         ON embeddings USING hnsw (embedding vector_cosine_ops)
         WITH (m = 16, ef_construction = 64);

    m: number of connections per layer (16 is good default)
    ef_construction: size of dynamic candidate list during index build (64 is good)

    Args:
        conn: psycopg2 connection object
    """
    with conn.cursor() as cur:
        # TODO: Execute the CREATE INDEX statement above
        # TODO: conn.commit()
        pass


def store_embeddings(conn, documents: list[dict]) -> None:
    """
    Exercise 3: Embed each document and store in pgvector.

    For each document:
    1. Create the text: f"{doc['title']}: {doc['content']}"
    2. Call get_embedding(text)
    3. Use execute_values() to bulk insert into the embeddings table

    Use execute_values() from psycopg2.extras for efficient bulk insert:
    execute_values(cur,
        "INSERT INTO embeddings (source, title, content, embedding) VALUES %s",
        [(doc["source"], doc["title"], doc["content"], embedding), ...]
    )

    Print progress for each document.

    Args:
        conn: psycopg2 connection object
        documents: List of document dicts to embed and store
    """
    rows = []
    print(f"Embedding {len(documents)} documents...")

    for i, doc in enumerate(documents):
        text = f"{doc['title']}: {doc['content']}"
        # TODO: Call get_embedding(text)
        # TODO: Append (doc["source"], doc["title"], doc["content"], embedding) to rows
        print(f"  [{i+1}/{len(documents)}] {doc['title']}")

    with conn.cursor() as cur:
        # TODO: Use execute_values() to bulk insert all rows
        # TODO: conn.commit()
        print(f"Stored {len(rows)} embeddings in pgvector")


def semantic_search(conn, query: str, top_k: int = 5) -> list[dict]:
    """
    Exercise 4: Query pgvector using cosine distance.

    1. Generate embedding for the query
    2. Use the <=> operator (cosine distance) to find nearest neighbors:

    SELECT source, title, content,
           1 - (embedding <=> %s::vector) AS similarity
    FROM embeddings
    ORDER BY embedding <=> %s::vector
    LIMIT %s;

    Note: <=> returns cosine DISTANCE (0=identical, 2=opposite)
    So similarity = 1 - distance

    Args:
        conn: psycopg2 connection object
        query: Natural language query
        top_k: Number of results to return

    Returns:
        List of dicts with source, title, content, similarity
    """
    query_embedding = get_embedding(query)

    with conn.cursor() as cur:
        # TODO: Execute the SELECT query above with:
        #   %s::vector = str(query_embedding)  (convert list to string for psycopg2)
        # TODO: Return [{"source": r[0], "title": r[1], "content": r[2], "similarity": r[3]} for r in cur.fetchall()]
        return []


if __name__ == "__main__":
    print("pgvector Semantic Search Engine")
    print("=" * 60)

    try:
        conn = connect_db()
        print("✓ Connected to PostgreSQL")
    except Exception as e:
        print(f"✗ Cannot connect to PostgreSQL: {e}")
        print("Make sure PostgreSQL is running (check with: pg_isready)")
        exit(1)

    print("\nExercise 1: Setup database and pgvector extension")
    setup_database(conn)

    print("\nExercise 2: Create HNSW index")
    create_hnsw_index(conn)

    print("\nExercise 3: Store embeddings")
    store_embeddings(conn, DOCUMENTATION_CORPUS)

    print("\nExercise 4: Semantic search queries")
    queries = [
        "How do I handle rate limits in my code?",
        "What model should I use for complex reasoning tasks?",
        "How do I protect against prompt injection attacks?",
        "How does streaming work with the API?",
    ]

    for query in queries:
        print(f"\nQuery: '{query}'")
        results = semantic_search(conn, query, top_k=3)
        for i, r in enumerate(results, 1):
            print(f"  {i}. [{r['similarity']:.4f}] {r['title']} ({r['source']})")
            print(f"     {r['content'][:80]}...")

    conn.close()
    print("\n✓ All exercises complete!")
