"""FastAPI orchestrator for the Summitline responsible-AI assistant.

The /approvals and /approvals/{req_id} endpoints are fully implemented below —
they just need app/approval.py's queue backend to exist for them to work.
"""
import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
from fastapi import FastAPI, Form, HTTPException

from app import approval, filters

load_dotenv()

app = FastAPI(title="Summitline Responsible AI Assistant")

_project = AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
_deployment = os.environ["MODEL_DEPLOYMENT"]


@app.post("/generate")
def generate(prompt: str = Form(...), requires_approval: bool = Form(False)) -> dict:
    # Exercise 1 - Step 6 Start
    raise NotImplementedError("Complete Exercise 1 Step 6")
    # Exercise 1 - Step 6 End


@app.get("/approvals")
def list_approvals() -> list[dict]:
    """Return every pending approval request."""
    return [
        {
            "id": r.id,
            "prompt": r.prompt,
            "draft_response": r.draft_response,
            "status": r.status,
            "reason": r.reason,
        }
        for r in approval.list_pending()
    ]


@app.post("/approvals/{req_id}")
def decide_approval(
    req_id: str,
    approved: bool = Form(...),
    reason: str = Form(""),
) -> dict:
    """Approve or reject a pending request by id."""
    try:
        req = approval.decide(req_id, approved=approved, reason=reason)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"approval {req_id} not found")
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    return {
        "id": req.id,
        "prompt": req.prompt,
        "draft_response": req.draft_response,
        "status": req.status,
        "reason": req.reason,
    }
