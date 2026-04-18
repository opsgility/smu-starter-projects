"""RAG chat endpoint."""
import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
from fastapi import FastAPI, Form

from . import retrieval

load_dotenv()

app = FastAPI(title="AI-103 RAG starter")

_project = AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
_deployment = os.environ["MODEL_DEPLOYMENT"]

SYSTEM = (
    "You are a Foundry assistant. Answer the user's question using ONLY the provided "
    "context. If the answer is not in the context, say so explicitly. Cite sources by "
    "filename in square brackets like [docs.md]."
)


@app.post("/chat")
def chat(message: str = Form(...)) -> dict:
    # TODO 1: hits = retrieval.search(message, k=5).
    # TODO 2: Build a context string: "\n\n".join(f"[{h['source']}] {h['chunk']}" for h in hits).
    # TODO 3: Prompt = f"Context:\n{context}\n\nQuestion: {message}".
    # TODO 4: Call _project.get_openai_client().responses.create(
    #              model=_deployment,
    #              input=[{"role":"system","content":SYSTEM},{"role":"user","content":prompt}]).
    # TODO 5: Return {"reply": response.output_text, "sources": [h["source"] for h in hits]}.
    raise NotImplementedError
