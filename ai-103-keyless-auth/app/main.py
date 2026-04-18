"""FastAPI chat endpoint — start with keys, migrate to keyless."""
import os

from dotenv import load_dotenv
from fastapi import FastAPI, Form
from openai import AzureOpenAI  # legacy starting point

load_dotenv()

app = FastAPI(title="AI-103 keyless auth starter")

# Starting state: API-key Azure OpenAI client. DO NOT SHIP.
_legacy_client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version="2024-10-21",
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
)
_deployment = os.environ["AZURE_OPENAI_DEPLOYMENT"]


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/chat")
def chat(message: str = Form(...)) -> dict:
    # TODO 1: Replace _legacy_client with AIProjectClient(endpoint=AZURE_AI_PROJECT_ENDPOINT,
    #         credential=DefaultAzureCredential()).get_openai_client().
    # TODO 2: Use client.responses.create(model=_deployment, input=message) instead of
    #         chat.completions.create.
    # TODO 3: Return {"reply": response.output_text}.
    response = _legacy_client.chat.completions.create(
        model=_deployment,
        messages=[{"role": "user", "content": message}],
    )
    return {"reply": response.choices[0].message.content}
