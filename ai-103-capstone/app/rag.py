"""Capstone RAG — retrieve from capstone-knowledge then answer."""
import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from dotenv import load_dotenv

load_dotenv()

PROJECT_ENDPOINT = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
SEARCH_ENDPOINT = os.environ["AZURE_SEARCH_ENDPOINT"]
INDEX = os.environ["AZURE_SEARCH_INDEX"]
EMBEDDING = os.environ["EMBEDDING_DEPLOYMENT"]
DEPLOYMENT = os.environ["MODEL_DEPLOYMENT"]
CRED = DefaultAzureCredential()


def answer(question: str) -> dict:
    # TODO 1: Embed `question` via _project.get_openai_client().embeddings.create(model=EMBEDDING, input=[question]).
    # TODO 2: Hybrid search SearchClient(SEARCH_ENDPOINT, INDEX, CRED).search(search_text=question,
    #         vector_queries=[VectorizedQuery(vector=vec, k_nearest_neighbors=5, fields="embedding")],
    #         select=["source","markdown"], top=5).
    # TODO 3: Build context = "\n\n".join(f"[{r['source']}] {r['markdown']}" for r in hits).
    # TODO 4: Call client.responses.create(model=DEPLOYMENT, input=[{"role":"system","content":
    #         "Answer using ONLY the context. Cite sources in [brackets]."},
    #         {"role":"user","content":f"Context:\n{context}\n\nQ: {question}"}]).
    # TODO 5: Return {"answer": response.output_text, "sources": [r["source"] for r in hits]}.
    raise NotImplementedError
