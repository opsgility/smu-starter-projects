"""Summitline Outfitters concierge — LEGACY key-based prototype.

This is the prototype you inherited from the Summitline Outfitters team. It
authenticates to Azure OpenAI using a static API key (`AZURE_OPENAI_API_KEY`)
read from the environment — a compliance and security liability.

Exercise 2 of Lab 2258 has you rewrite this file end-to-end:

    - Drop `from openai import AzureOpenAI`.
    - Replace the key-based client with:
        - `AIProjectClient` from `azure.ai.projects`
        - `DefaultAzureCredential` from `azure.identity`
        - `project.get_openai_client()` for the OpenAI surface
    - Switch from `chat.completions.create(messages=...)` to
      `responses.create(input=...)` and return `response.output_text`.
    - Read `AZURE_AI_PROJECT_ENDPOINT` and `AZURE_OPENAI_DEPLOYMENT` from
      `.env` — remove all reads of `AZURE_OPENAI_API_KEY` and
      `AZURE_OPENAI_ENDPOINT`.
"""
import os

# Exercise 2 - Step 5: replace the import below with:
#   from azure.ai.projects import AIProjectClient
#   from azure.identity import DefaultAzureCredential
from openai import AzureOpenAI

from dotenv import load_dotenv
from fastapi import FastAPI, Form

load_dotenv()

app = FastAPI(title="Summitline Outfitters Concierge (LEGACY key-auth)")

# Exercise 2 - Step 5 Start
_deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4.1")
_openai = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_version="2024-10-21",
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/chat")
def chat(message: str = Form(...)) -> dict:
    response = _openai.chat.completions.create(
        model=_deployment,
        messages=[{"role": "user", "content": message}],
    )
    return {"reply": response.choices[0].message.content}


@app.on_event("shutdown")
def _close() -> None:
    _openai.close()
# Exercise 2 - Step 5 End
