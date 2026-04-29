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
    # Exercise 1 - Step 6 Start
    raise NotImplementedError("Complete Exercise 1 Step 6")
    # Exercise 1 - Step 6 End
