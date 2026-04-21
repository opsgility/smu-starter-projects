"""Azure AI Content Safety wrapper used as a pre and post filter.

Exercise 1 (Lab 2263) — implement `check()` to call `analyze_text` and return a
`{blocked, categories}` dict. Severity threshold 4 matches Microsoft's default
"medium" block level. Categories returned by analyze_text are Hate, SelfHarm,
Sexual, and Violence with severities 0 / 2 / 4 / 6.
"""
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
    """Return {"blocked": bool, "categories": {name: severity}}.

    TODO (Exercise 1 Step 6): Call `_client.analyze_text(AnalyzeTextOptions(text=text))`,
    build a `{ca.category: ca.severity for ca in result.categories_analysis}` dict,
    and set `blocked=True` when any severity is >= SEVERITY_THRESHOLD.
    """
    # TODO (Exercise 1 Step 6): call analyze_text and build the result dict.
    # TODO (Exercise 1 Step 6): build `categories` dict from result.categories_analysis.
    # TODO (Exercise 1 Step 6): compute `blocked` by comparing each severity to SEVERITY_THRESHOLD.
    raise NotImplementedError("Implement filters.check() in Exercise 1, Step 6.")
