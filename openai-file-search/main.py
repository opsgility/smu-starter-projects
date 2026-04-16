"""
OpenAI File Search & Vector Stores API
Course 202 - Lesson 8: File Search Integration

Exercises:
1. Create a vector store and upload documents
2. Query the vector store using the file_search built-in tool
3. Verify file search is invoked automatically (not manual retrieval)
4. Manage vector store lifecycle (list files, check status)

IMPORTANT: OPENAI_API_KEY and OPENAI_BASE_URL are pre-configured in your
environment automatically.
"""
from openai import OpenAI
import os
import json
import tempfile
from pathlib import Path

client = OpenAI()

# Sample technical documents to upload to the vector store
TECHNICAL_DOCUMENTS = {
    "openai_authentication.txt": """# OpenAI API Authentication Guide

## API Keys
The OpenAI API uses API keys for authentication. Your API key should be kept secret
and never exposed in client-side code or committed to version control.

## Setting Up Your Key
Store your API key as an environment variable named OPENAI_API_KEY:
  export OPENAI_API_KEY="sk-..."

## Organization and Project Keys
You can create project-scoped keys in the OpenAI dashboard under Settings > API Keys.
Project keys can be restricted to specific models and usage limits.

## Key Rotation
Rotate your API keys regularly:
1. Create a new key in the dashboard
2. Update your application configuration
3. Test the new key works
4. Delete the old key
5. Wait 24 hours before final deactivation

## Troubleshooting
- 401 Unauthorized: Invalid or expired API key
- 403 Forbidden: Key doesn't have permission for the requested model
- Check your key status at platform.openai.com/account/api-keys
""",

    "openai_rate_limits.txt": """# OpenAI Rate Limits Guide

## Understanding Rate Limits
Rate limits are applied per model, per organization, and per minute. There are three types:
- RPM (Requests Per Minute): number of API calls per minute
- TPM (Tokens Per Minute): total tokens processed per minute
- RPD (Requests Per Day): total requests per day for some models

## Tier Structure
OpenAI uses usage tiers:
- Tier 1 (default): 500 RPM, 30,000 TPM for GPT-4.1
- Tier 2: 5,000 RPM, 450,000 TPM (requires $50 spend)
- Tier 3: 5,000 RPM, 800,000 TPM (requires $100 spend)
- Tier 4: 10,000 RPM, 2,000,000 TPM (requires $250 spend)
- Tier 5: 30,000 RPM, 150,000,000 TPM (requires $1,000 spend)

## Handling Rate Limit Errors
When you receive a 429 error:
1. Check the Retry-After header for the wait time
2. Implement exponential backoff: wait 2^n seconds (1s, 2s, 4s, 8s...)
3. Add jitter to prevent thundering herd: random(0, 1) * wait_time
4. Use a queue to smooth out traffic spikes

## Best Practices
- Monitor your usage in the OpenAI dashboard
- Set up usage alerts to avoid unexpected costs
- Use the Batch API for non-time-sensitive workloads
- Cache responses for repeated identical requests
""",

    "openai_models_guide.txt": """# OpenAI Models Guide - April 2026

## GPT-4.1 Family

### GPT-4.1 (Flagship)
- Context window: 1,000,000 tokens
- Best for: Complex analysis, code generation, reasoning
- Pricing: $2.00/1M input, $8.00/1M output
- Max output: 32,768 tokens

### GPT-4.1-mini
- Context window: 1,000,000 tokens
- Best for: Most production tasks, balanced cost/quality
- Pricing: $0.40/1M input, $1.60/1M output

### GPT-4.1-nano
- Context window: 1,000,000 tokens
- Best for: Classification, routing, simple tasks
- Pricing: $0.10/1M input, $0.40/1M output

## Reasoning Models

### o3
- Extended chain-of-thought reasoning
- Best for: Math, science, complex logic, research
- Pricing: $10.00/1M input, $40.00/1M output
- reasoning_effort: low/medium/high (controls cost vs. accuracy)

### o4-mini
- Efficient reasoning model
- Best for: Code, math, analysis at lower cost than o3
- Pricing: $1.10/1M input, $4.40/1M output

## Choosing the Right Model
1. Simple classification/routing -> GPT-4.1-nano
2. General purpose -> GPT-4.1-mini
3. Complex analysis or code -> GPT-4.1
4. Math, logic, research -> o3 or o4-mini
5. Vision tasks -> GPT-4o or GPT-4.1 (supports images)
""",

    "openai_embeddings_guide.txt": """# OpenAI Embeddings API Guide

## Available Embedding Models

### text-embedding-3-small
- Dimensions: 1536 (default) or custom (down to 256)
- Best for: Most production use cases
- Pricing: $0.02/1M tokens
- Performance: Strong on MTEB benchmark

### text-embedding-3-large
- Dimensions: 3072 (default) or custom
- Best for: High-stakes retrieval, multilingual content
- Pricing: $0.13/1M tokens

## Generating Embeddings
response = client.embeddings.create(
    model="text-embedding-3-small",
    input="Your text here",
    dimensions=1536  # optional: reduce for cost savings
)
embedding = response.data[0].embedding  # list of floats

## Dimension Reduction
The dimensions parameter lets you reduce embedding size:
- Smaller = cheaper storage and faster similarity search
- But lower quality at retrieval
- 512 dimensions retains ~98% of quality vs 1536

## Similarity Search
Use cosine similarity or dot product for finding similar vectors.
Since embeddings are normalized, these give the same result.

## Best Practices
- Chunk documents to 200-400 tokens for best retrieval
- Include titles/headers in chunks for context
- Store embeddings in a vector database (pgvector, Pinecone, Weaviate)
- Refresh embeddings when model is updated
""",

    "openai_responses_api.txt": """# OpenAI Responses API Reference

## Overview
The Responses API is the modern, stateful API replacing Chat Completions.
It supports built-in tools, multi-turn conversations, and streaming.

## Basic Usage
response = client.responses.create(
    model="gpt-4.1",
    input="What is the capital of France?"
)
print(response.output_text)

## Multi-Turn Conversations
Use previous_response_id to maintain conversation state:
first = client.responses.create(model="gpt-4.1", input="My name is Alice")
second = client.responses.create(
    model="gpt-4.1",
    input="What is my name?",
    previous_response_id=first.id
)

## Built-in Tools
Available tools: web_search, file_search, code_interpreter, computer_use

## Tool Calling
response = client.responses.create(
    model="gpt-4.1",
    input="What's the weather in Paris?",
    tools=[{"type": "function", "name": "get_weather", ...}]
)

## Streaming
with client.responses.stream(model="gpt-4.1", input="Tell me a story") as s:
    for text in s.text_stream:
        print(text, end="", flush=True)

## Structured Output
response = client.responses.parse(
    model="gpt-4.1",
    input="Extract the price",
    text_format=MyPydanticModel
)
result = response.output_parsed
""",
}

# Test questions for Q&A evaluation
TEST_QUESTIONS = [
    "How do I handle a 429 rate limit error in my code?",
    "What is the difference between GPT-4.1-mini and GPT-4.1-nano?",
    "How do I reduce the size of my embeddings to save costs?",
    "What is the previous_response_id parameter used for?",
    "How often should I rotate my API keys?",
    "What are the pricing tiers for OpenAI API access?",
    "How do I use streaming with the Responses API?",
    "What is the recommended chunk size for embeddings?",
]


def create_vector_store(name: str) -> str:
    """
    Exercise 1a: Create a vector store.

    Use client.vector_stores.create(name=name).
    Return the vector store ID (vs.id).

    Args:
        name: Display name for the vector store

    Returns:
        Vector store ID string
    """
    # TODO: vs = client.vector_stores.create(name=name)
    # TODO: print(f"Created vector store: {vs.id}")
    # TODO: return vs.id
    return ""


def upload_documents_to_vector_store(vector_store_id: str) -> None:
    """
    Exercise 1b: Upload documents to the vector store.

    For each document in TECHNICAL_DOCUMENTS:
    1. Write the content to a temporary file
    2. Open the file in binary mode
    3. Use client.vector_stores.files.upload_and_poll() to upload and wait for indexing

    upload_and_poll() blocks until the file is fully indexed.

    Args:
        vector_store_id: The ID of the vector store to upload to
    """
    print(f"Uploading {len(TECHNICAL_DOCUMENTS)} documents...")

    for filename, content in TECHNICAL_DOCUMENTS.items():
        print(f"  Uploading {filename}...")

        # Write to a temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt',
                                        delete=False, prefix=filename) as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        try:
            # TODO: Open tmp_path in "rb" mode
            # TODO: client.vector_stores.files.upload_and_poll(
            #           vector_store_id=vector_store_id, file=f)
            # TODO: print(f"    ✓ {filename} indexed")
            pass
        finally:
            os.unlink(tmp_path)


def query_with_file_search(vector_store_id: str, question: str) -> str:
    """
    Exercise 2: Query the vector store using the file_search built-in tool.

    Use client.responses.create() with the file_search tool.
    The model will automatically search the vector store and include
    retrieved context in its response.

    tools = [{"type": "file_search", "vector_store_ids": [vector_store_id]}]

    Args:
        vector_store_id: The vector store to search
        question: The question to answer

    Returns:
        The model's answer based on retrieved context
    """
    # TODO: Call client.responses.create() with:
    #   model = "gpt-4.1-mini"
    #   input = question
    #   tools = [{"type": "file_search", "vector_store_ids": [vector_store_id]}]
    # TODO: Verify that file_search was invoked (check response.output for file_search_call)
    # TODO: Return response.output_text
    return ""


def verify_file_search_invoked(response) -> bool:
    """
    Exercise 3: Verify that file_search tool was automatically invoked.

    Check response.output for an item with type == "file_search_call".
    Return True if file_search was used, False if the model answered without it.
    """
    # TODO: Iterate over response.output
    # TODO: Check if any item has type == "file_search_call"
    return False


def evaluate_qa_system(vector_store_id: str) -> None:
    """
    Exercise 4: Run the Q&A system on all test questions.

    For each question:
    - Query the vector store
    - Check that file_search was invoked
    - Print the answer and tool invocation status
    - Track: correct source documents retrieved?
    """
    correct_retrievals = 0
    total = len(TEST_QUESTIONS)

    print(f"\nEvaluating Q&A system on {total} questions...")
    print("-" * 60)

    for i, question in enumerate(TEST_QUESTIONS, 1):
        print(f"\n{i}. Q: {question}")
        answer = query_with_file_search(vector_store_id, question)
        print(f"   A: {answer[:150]}..." if len(answer) > 150 else f"   A: {answer}")

    print(f"\n\nEvaluation complete: {total} questions answered")


if __name__ == "__main__":
    print("OpenAI File Search & Vector Stores")
    print("=" * 60)

    # Exercise 1: Create vector store and upload documents
    print("\nExercise 1: Create vector store and upload documents")
    vs_id = create_vector_store("Technical Documentation Store")
    if vs_id:
        upload_documents_to_vector_store(vs_id)
        print(f"Vector store ready: {vs_id}")

        # Exercise 2 & 3: Query with file_search
        print("\nExercise 2: Query with file_search built-in tool")
        test_q = TEST_QUESTIONS[0]
        print(f"Question: {test_q}")
        answer = query_with_file_search(vs_id, test_q)
        print(f"Answer: {answer}")

        # Exercise 4: Full evaluation
        print("\nExercise 4: Evaluate on all test questions")
        evaluate_qa_system(vs_id)
