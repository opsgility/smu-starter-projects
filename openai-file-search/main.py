"""
File Search Integration
Course 202 - Lesson 8: OpenAI File Search & Vector Stores API

Build a document Q&A assistant using the Responses API file_search
built-in tool over uploaded technical documents.

IMPORTANT: OPENAI_API_KEY and OPENAI_BASE_URL are pre-configured in your
environment automatically. Do NOT set them manually.
"""
from openai import OpenAI
import json
import time

client = OpenAI()

# Sample documents to upload and search
DOCUMENTS = {
    "python_best_practices.txt": """Python Best Practices Guide

1. Use virtual environments for every project (python -m venv .venv)
2. Pin dependencies in requirements.txt with exact versions
3. Use type hints for all public functions
4. Write docstrings for all modules, classes, and functions
5. Follow PEP 8: 4-space indentation, 79-char line limit
6. Use f-strings for string formatting (Python 3.6+)
7. Prefer list/dict/set comprehensions over map/filter
8. Use context managers (with statements) for resource management
9. Handle exceptions specifically, not bare except
10. Run black and ruff for formatting and linting
""",
    "api_security_guide.txt": """API Security Guide

Authentication:
- Always use HTTPS, never HTTP
- Store API keys in environment variables, never hardcode
- Rotate API keys every 90 days
- Use the principle of least privilege for API permissions

Input Validation:
- Validate all inputs at the API boundary
- Sanitize strings to prevent injection attacks
- Enforce strict JSON schemas on all endpoints
- Rate limit by IP and by user ID

Secrets Management:
- Use a secrets manager (AWS Secrets Manager, Azure Key Vault)
- Never log secrets or API keys
- Audit access to secrets regularly
""",
    "database_optimization.txt": """Database Optimization Guide

Indexing Strategy:
- Add indexes on columns used in WHERE, JOIN, and ORDER BY
- Use composite indexes for multi-column queries
- HNSW indexes for vector similarity search in pgvector
- Monitor slow queries with pg_stat_statements

Query Optimization:
- Use EXPLAIN ANALYZE to profile query plans
- Avoid SELECT * — specify needed columns
- Use pagination (LIMIT/OFFSET or cursor-based) for large result sets
- Batch writes in transactions to reduce round trips

Connection Pooling:
- Use PgBouncer or connection pooling in your ORM
- Set max_connections based on available RAM
- Monitor idle connections and set idle timeouts
""",
}


def create_vector_store(name: str) -> str:
    """
    Exercise 1: Create a new OpenAI vector store.

    Use client.vector_stores.create(name=name)
    Returns the vector store ID.
    """
    # TODO: Call client.vector_stores.create(name=name)
    # TODO: Return vector_store.id
    pass


def upload_documents(vector_store_id: str, documents: dict) -> None:
    """
    Exercise 2: Upload documents to the vector store.

    For each document name and content:
    1. Create an in-memory file-like object using io.BytesIO
    2. Upload using client.vector_stores.files.upload_and_poll(
           vector_store_id=vector_store_id,
           file=(filename, content_bytes, "text/plain")
       )
    3. Print upload status for each file

    Import io at the top of the function.
    """
    import io
    print(f"Uploading {len(documents)} documents to vector store {vector_store_id}...")
    # TODO: For each filename, content in documents.items():
    #   content_bytes = content.encode("utf-8")
    #   file_tuple = (filename, io.BytesIO(content_bytes), "text/plain")
    #   result = client.vector_stores.files.upload_and_poll(
    #       vector_store_id=vector_store_id, file=file_tuple
    #   )
    #   print(f"  {filename}: {result.status}")
    pass


def ask_with_file_search(question: str, vector_store_id: str) -> str:
    """
    Exercise 3: Answer a question using the file_search built-in tool.

    Use client.responses.create() with:
    - model="gpt-4.1-mini"
    - input=[{"role": "user", "content": question}]
    - tools=[{"type": "file_search", "vector_store_ids": [vector_store_id]}]

    Returns the response text.
    """
    # TODO: Call client.responses.create() with file_search tool
    # TODO: Return response.output_text
    pass


if __name__ == "__main__":
    print("File Search Integration — Course 202 Lesson 8")
    print("=" * 48)

    # Create vector store and upload documents
    vs_id = create_vector_store("Course202-Docs")
    if vs_id:
        upload_documents(vs_id, DOCUMENTS)

        # Ask questions
        questions = [
            "What are the top 3 Python best practices?",
            "How often should I rotate API keys and where should I store them?",
            "What database index type should I use for vector similarity search?",
        ]

        for question in questions:
            print(f"\nQuestion: {question}")
            answer = ask_with_file_search(question, vs_id)
            if answer:
                print(f"Answer: {answer[:300]}...")
