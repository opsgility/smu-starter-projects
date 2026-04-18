"""Azure AI Content Safety wrapper used as a pre and post filter."""
import os

from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()

_client = ContentSafetyClient(
    endpoint=os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["AZURE_CONTENT_SAFETY_KEY"]),
)

SEVERITY_THRESHOLD = 4


def check(text: str) -> dict:
    """Return {"blocked": bool, "categories": {name: severity}}."""
    # TODO 1: call _client.analyze_text(AnalyzeTextOptions(text=text)) and capture result.
    # TODO 2: build categories dict from result.categories_analysis — {ca.category: ca.severity}.
    # TODO 3: return blocked=True when any severity >= SEVERITY_THRESHOLD.
    raise NotImplementedError
