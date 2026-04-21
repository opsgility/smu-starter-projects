"""FastAPI orchestrator for the Summitline responsible-AI assistant.

Exercise 1 (Lab 2263) — TODO 1, 2, 3 in /generate (pre-filter, Responses API call, post-filter).
Exercise 3 (Lab 2263) — TODO 4 in /generate (approval branch).

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
    """Generate a reply for a Summitline customer prompt, gated by Content Safety.

    Pre-filter the prompt, call the Responses API, post-filter the draft, then
    either return the draft directly or park it in the approval queue.
    """
    # TODO 1 (Exercise 1 Step 7): pre-filter `prompt` with filters.check().
    # If pre["blocked"], raise HTTPException(status_code=400,
    # detail={"stage": "pre", **pre}).

    # TODO 2 (Exercise 1 Step 7): call the Responses API.
    # with _project.get_openai_client() as client:
    #     response = client.responses.create(model=_deployment, input=prompt)
    # draft = response.output_text

    # TODO 3 (Exercise 1 Step 7): post-filter `draft` with filters.check().
    # If post["blocked"], raise HTTPException(status_code=422,
    # detail={"stage": "post", **post}).

    # TODO 4 (Exercise 3 Step 2): if requires_approval, submit to approval queue
    # and return {"status": "pending", "approval_id": approval.submit(prompt, draft)}.
    # Otherwise return {"reply": draft}.
    raise NotImplementedError(
        "Implement /generate: pre-filter, Responses API, post-filter, approval branch."
    )


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
