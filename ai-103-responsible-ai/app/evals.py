"""Run Foundry evaluations: groundedness, relevance, violence, hate.

Exercise 2 (Lab 2263) — implement `run()` with:
- Quality evaluators (GroundednessEvaluator, RelevanceEvaluator) using a
  `model_config` that points at your gpt-4.1-mini deployment.
- Safety evaluators (ViolenceEvaluator, HateUnfairnessEvaluator) using
  `azure_ai_project` (the full project endpoint) + DefaultAzureCredential.
- `evaluate()` with column mappings for each evaluator against EVAL_DATASET.

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

    # TODO 1 (Exercise 2 Step 3): build `model_config` for the quality evaluators.
    # Use project_endpoint.split("/api/projects")[0] as azure_endpoint,
    # `deployment` as azure_deployment, and "2024-10-21" as api_version.

    # TODO 2 (Exercise 2 Step 3): construct the four evaluators in an `evaluators` dict:
    #   - "groundedness": GroundednessEvaluator(model_config)
    #   - "relevance":    RelevanceEvaluator(model_config)
    #   - "violence":     ViolenceEvaluator(azure_ai_project=project_endpoint,
    #                                       credential=DefaultAzureCredential())
    #   - "hate_unfairness": HateUnfairnessEvaluator(azure_ai_project=project_endpoint,
    #                                                credential=DefaultAzureCredential())

    # TODO 3 (Exercise 2 Step 3): build `evaluator_config` with per-evaluator column_mapping
    # entries like {"query": "${data.query}", "response": "${data.response}", ...},
    # then return evaluate(data=os.environ["EVAL_DATASET"], evaluators=evaluators,
    # evaluator_config=evaluator_config, azure_ai_project=project_endpoint,
    # output_path="./eval_output.json").
    raise NotImplementedError("Implement app.evals.run() in Exercise 2, Step 3.")


if __name__ == "__main__":
    result = run()
    print(result.get("studio_url", "(no studio url)"))
