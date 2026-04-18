"""Run Foundry evaluations: groundedness, relevance, violence, hate."""
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
    project_endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
    deployment = os.environ["MODEL_DEPLOYMENT"]

    # Model config for AI-assisted (quality) evaluators.
    model_config = {
        "azure_endpoint": project_endpoint.split("/api/projects")[0],
        "azure_deployment": deployment,
        "api_version": "2024-10-21",
    }

    # TODO 1: Construct quality evaluators: GroundednessEvaluator(model_config),
    #         RelevanceEvaluator(model_config).
    # TODO 2: Construct safety evaluators: ViolenceEvaluator(azure_ai_project=project_endpoint,
    #         credential=DefaultAzureCredential()), same for HateUnfairnessEvaluator.
    # TODO 3: Call evaluate(data=os.environ["EVAL_DATASET"], evaluators={...},
    #         evaluator_config={...}, azure_ai_project=project_endpoint,
    #         output_path="./eval_output.json") and return the returned dict.
    raise NotImplementedError


if __name__ == "__main__":
    result = run()
    print(result.get("studio_url", "(no studio url)"))
