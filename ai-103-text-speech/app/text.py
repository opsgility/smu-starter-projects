"""Text analysis: structured extraction (LLM) + sentiment/key phrases (Language)."""
import json
import os

from azure.ai.projects import AIProjectClient
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

PROJECT_ENDPOINT = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
MODEL = os.environ["MODEL_DEPLOYMENT"]

_lang = TextAnalyticsClient(
    endpoint=os.environ["LANGUAGE_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["LANGUAGE_KEY"]),
)

EXTRACTION_PROMPT = (
    "Extract the following from the provided text and return STRICT JSON: "
    '{ "people": [...], "organizations": [...], "products": [...], "summary": "..." }. '
    "Return ONLY the JSON object."
)


def analyze(content: str) -> dict:
    """Combined sentiment + key phrases via the Language service."""
    # TODO 1: sent = _lang.analyze_sentiment([content])[0]
    # TODO 2: kp = _lang.extract_key_phrases([content])[0]
    # TODO 3: return {"sentiment": sent.sentiment,
    #                  "confidence": sent.confidence_scores.as_dict(),
    #                  "key_phrases": list(kp.key_phrases)}.
    raise NotImplementedError


def extract(content: str) -> dict:
    """Structured extraction via the LLM."""
    with AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=DefaultAzureCredential()) as project:
        with project.get_openai_client() as client:
            # TODO 4: Call client.responses.create(model=MODEL, input=[
            #             {"role":"system","content":EXTRACTION_PROMPT},
            #             {"role":"user","content":content}
            #         ]). Return json.loads(response.output_text).
            raise NotImplementedError
