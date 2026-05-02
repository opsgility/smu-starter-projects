"""Run Foundry evaluations: groundedness, relevance, violence, hate.

`python -m app.evals` prints the Foundry studio URL and writes eval_output.json.
"""
import os

from azure.ai.evaluation import (
    GroundednessEvaluator,
    HateUnfairnessEvaluator,
    RelevanceEvaluator,
    ViolenceEvaluator,
    evaluate,
)
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()


def run() -> dict:
    """Execute all four evaluators against EVAL_DATASET and return the result dict."""
    project_endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
    deployment = os.environ["MODEL_DEPLOYMENT"]

    # Exercise 2 - Step 1 Start
    raise NotImplementedError("Complete Exercise 2 Step 1")
    # Exercise 2 - Step 1 End


if __name__ == "__main__":
    result = run()
    print(result.get("studio_url", "(no studio url)"))
