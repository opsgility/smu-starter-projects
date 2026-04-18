"""Responsible-AI orchestrator: pre-filter → model → post-filter → optional approval."""
import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
from fastapi import FastAPI, Form, HTTPException

from . import approval, filters

load_dotenv()

app = FastAPI(title="AI-103 responsible AI starter")

_project = AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
_deployment = os.environ["MODEL_DEPLOYMENT"]


@app.post("/generate")
def generate(prompt: str = Form(...), requires_approval: bool = Form(False)) -> dict:
    # TODO 1: Call filters.check(prompt); if blocked=True, raise HTTPException(400, detail=...).
    # TODO 2: Use _project.get_openai_client().responses.create(model=_deployment, input=prompt)
    #         to produce a draft response (response.output_text).
    # TODO 3: Run filters.check(draft); if blocked, raise HTTPException(422, ...).
    # TODO 4: If requires_approval, call approval.submit(prompt, draft) and return
    #         {"status": "pending", "approval_id": id}. Otherwise return {"reply": draft}.
    raise NotImplementedError


@app.get("/approvals")
def list_approvals() -> list:
    return [vars(r) for r in approval.list_pending()]


@app.post("/approvals/{req_id}")
def decide(req_id: str, approved: bool = Form(...), reason: str = Form("")) -> dict:
    updated = approval.decide(req_id, approved, reason)
    return vars(updated)
