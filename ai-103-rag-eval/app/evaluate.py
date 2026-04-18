"""Run Foundry evaluations against eval_data.jsonl."""
import os

from azure.ai.evaluation import GroundednessEvaluator, RelevanceEvaluator, evaluate
from dotenv import load_dotenv

from . import retrieval

load_dotenv()


def chat_target(query: str) -> dict:
    """Used as the target= parameter to evaluate(). Reproduces /chat without HTTP."""
    hits = retrieval.search(query, k=5)
    context = "\n\n".join(f"[{h['source']}] {h['chunk']}" for h in hits)
    # TODO 1: Call the project's openai client to generate a response (same as app.main).
    # TODO 2: Return {"response": <text>, "context": context}.
    raise NotImplementedError


def main() -> None:
    project_endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
    deployment = os.environ["MODEL_DEPLOYMENT"]
    model_config = {
        "azure_endpoint": project_endpoint.split("/api/projects")[0],
        "azure_deployment": deployment,
        "api_version": "2024-10-21",
    }

    # TODO 3: Call evaluate(
    #             data="eval_data.jsonl",
    #             target=chat_target,
    #             evaluators={
    #                 "groundedness": GroundednessEvaluator(model_config),
    #                 "relevance": RelevanceEvaluator(model_config),
    #             },
    #             evaluator_config={
    #                 "groundedness": {"column_mapping": {"query":"${data.query}",
    #                                                       "response":"${outputs.response}",
    #                                                       "context":"${outputs.context}"}},
    #                 "relevance": {"column_mapping": {"query":"${data.query}",
    #                                                    "response":"${outputs.response}"}},
    #             },
    #             azure_ai_project=project_endpoint,
    #             output_path="./eval_output.json",
    #         )
    # TODO 4: Print result["studio_url"] and result["metrics"].
    raise NotImplementedError


if __name__ == "__main__":
    main()
