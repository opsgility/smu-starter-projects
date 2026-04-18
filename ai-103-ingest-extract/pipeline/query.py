"""Sample hybrid query against the extracted index."""
import os
import sys

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ["AZURE_SEARCH_ENDPOINT"]
INDEX = os.environ["AZURE_SEARCH_INDEX"]
PROJECT_ENDPOINT = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
EMBEDDING = os.environ["EMBEDDING_DEPLOYMENT"]
CRED = DefaultAzureCredential()


def _embed(text: str) -> list[float]:
    with AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=CRED) as project:
        with project.get_openai_client() as client:
            return client.embeddings.create(model=EMBEDDING, input=[text]).data[0].embedding


def query(text: str, k: int = 5) -> list[dict]:
    vec = _embed(text)
    vq = VectorizedQuery(vector=vec, k_nearest_neighbors=k, fields="embedding")
    client = SearchClient(ENDPOINT, INDEX, CRED)
    results = client.search(
        search_text=text,
        vector_queries=[vq],
        select=["id", "source", "doc_type", "markdown"],
        top=k,
        query_type="semantic",
        semantic_configuration_name="default",
    )
    return [
        {"score": r["@search.score"], "source": r["source"], "doc_type": r.get("doc_type",""), "snippet": r["markdown"][:200]}
        for r in results
    ]


if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "What is the invoice total?"
    for hit in query(q):
        print(f"{hit['score']:.3f}  {hit['source']:30} ({hit['doc_type']})  {hit['snippet']}")
