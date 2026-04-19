"""
Persistent Embedding Store with pgvector
Course 202 - Lesson 4: Vector Storage with pgvector

Build a persistent embedding store that chunks a documentation corpus,
embeds each chunk, stores in pgvector, and retrieves semantically similar
chunks for any query.

Database connection: PostgreSQL with pgvector is available at:
  host=localhost, dbname=vectordb, user=postgres, password=postgres

IMPORTANT: OPENAI_API_KEY and OPENAI_BASE_URL are pre-configured in your
environment automatically. Do NOT set them manually.
"""
from openai import OpenAI
import psycopg2
import json

client = OpenAI()

# Database connection config
DB_CONFIG = {
    "host": "localhost",
    "dbname": "vectordb",
    "user": "postgres",
    "password": "postgres",
    "port": 5432,
}

# Sample documentation corpus to index
DOCUMENTS = [
    {"title": "Authentication Guide", "content": "To authenticate with the API, include your API key in the Authorization header as 'Bearer YOUR_API_KEY'. Keys can be created in the API settings dashboard. Rotate keys every 90 days for security."},
    {"title": "Rate Limiting", "content": "The API enforces rate limits of 1000 requests per minute for standard accounts and 10000 for enterprise. When exceeded, the API returns HTTP 429. Implement exponential backoff starting at 1 second."},
    {"title": "Webhook Configuration", "content": "Configure webhooks by providing a publicly accessible HTTPS endpoint in your settings. Events are sent as POST requests with JSON payloads. Verify the signature using the X-Signature header and your webhook secret."},
    {"title": "Data Retention Policy", "content": "User data is retained for 90 days after account deletion. Logs are kept for 365 days for compliance. Request data exports via the admin panel before deletion. Encrypted backups are stored for 7 years."},
    {"title": "SDK Installation", "content": "Install the Python SDK with: pip install our-sdk>=2.0. The SDK supports Python 3.9+. Initialize with sdk.Client(api_key=YOUR_KEY). The SDK auto-retries on transient errors with jitter."},
    {"title": "Error Codes Reference", "content": "400: Bad request - check your JSON syntax. 401: Unauthorized - verify your API key. 403: Forbidden - insufficient permissions. 404: Not found - check the resource ID. 429: Rate limited - back off and retry. 500: Server error - retry with backoff."},
    {"title": "Batch Processing", "content": "Use the /batch endpoint to submit up to 1000 requests in a single API call. Batch jobs process asynchronously. Poll /batch/{id}/status for completion. Results are available for 24 hours after completion."},
    {"title": "Pagination Guide", "content": "List endpoints return paginated results with a default page size of 20 (max 100). Use the cursor parameter from the response's next_cursor field to fetch subsequent pages. An empty next_cursor indicates the last page."},
    {"title": "Audit Logging", "content": "All API calls are logged with user ID, timestamp, endpoint, response code, and latency. Audit logs are available via the /audit endpoint with date range filtering. Export as CSV or JSON for compliance reporting."},
    {"title": "Multi-tenant Architecture", "content": "Each tenant has isolated data in separate database schemas. Cross-tenant data access is prevented at the application and database layer. Tenant IDs are validated on every request via JWT claims."},
]

CHUNK_SIZE = 200  # characters per chunk


def get_connection():
    """Create a database connection."""
    return psycopg2.connect(**DB_CONFIG)


def setup_database():
    """
    Exercise 1: Set up the pgvector database schema.

    Execute the following SQL:
    1. CREATE EXTENSION IF NOT EXISTS vector
    2. CREATE TABLE IF NOT EXISTS embeddings (
           id SERIAL PRIMARY KEY,
           title TEXT,
           chunk_text TEXT,
           embedding vector(1536)
       )
    3. CREATE INDEX IF NOT EXISTS embeddings_idx
       ON embeddings USING hnsw (embedding vector_cosine_ops)
    """
    # TODO: Connect to the database with get_connection()
    # TODO: Execute the three SQL statements above
    # TODO: Commit and close the connection
    print("Database setup complete.")


def embed_text(text: str) -> list[float]:
    """Get an embedding for a text string using text-embedding-3-small."""
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )
    return response.data[0].embedding


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE) -> list[str]:
    """Split text into overlapping chunks of approximately chunk_size characters."""
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        if current_length + len(word) > chunk_size and current_chunk:
            chunks.append(" ".join(current_chunk))
            # 20% overlap
            overlap = max(1, len(current_chunk) // 5)
            current_chunk = current_chunk[-overlap:]
            current_length = sum(len(w) for w in current_chunk)
        current_chunk.append(word)
        current_length += len(word) + 1

    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks


def index_documents(documents: list[dict]):
    """
    Exercise 2: Chunk, embed, and store documents in pgvector.

    For each document:
    1. Split content into chunks using chunk_text()
    2. Embed each chunk with embed_text()
    3. INSERT INTO embeddings (title, chunk_text, embedding) VALUES (...)

    Use psycopg2 and commit after all inserts.
    """
    print(f"Indexing {len(documents)} documents...")
    # TODO: Connect to database
    # TODO: For each document, chunk the content, embed each chunk
    # TODO: INSERT each chunk + embedding into the embeddings table
    # TODO: Commit and close
    print("Indexing complete.")


def semantic_search(query: str, top_k: int = 5) -> list[dict]:
    """
    Exercise 3: Query the vector store for the most similar chunks.

    Steps:
    1. Embed the query with embed_text()
    2. Run: SELECT title, chunk_text, 1 - (embedding <=> %s::vector) AS score
             FROM embeddings ORDER BY embedding <=> %s::vector LIMIT %s
    3. Return list of dicts with title, chunk_text, score

    The <=> operator is pgvector's cosine distance operator.
    Score = 1 - cosine_distance = cosine_similarity.
    """
    # TODO: Embed the query
    # TODO: Execute the SELECT query with the embedding as parameter
    # TODO: Return results as list of dicts
    pass


if __name__ == "__main__":
    print("Persistent Embedding Store — Course 202 Lesson 4")
    print("=" * 50)

    setup_database()
    index_documents(DOCUMENTS)

    queries = [
        "How do I authenticate with the API?",
        "What happens when I hit rate limits?",
        "How long is my data kept?",
    ]

    for query in queries:
        print(f"\nQuery: '{query}'")
        results = semantic_search(query, top_k=3)
        if results:
            for r in results:
                print(f"  [{r['score']:.3f}] {r['title']}: {r['chunk_text'][:80]}...")
