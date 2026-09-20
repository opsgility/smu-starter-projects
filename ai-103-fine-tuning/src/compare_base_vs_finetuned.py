"""Side-by-side comparison of the base gpt-4.1-mini deployment vs the fine-tuned deployment.

Exercise 7 Steps 2-4.

Reads   data/held_out_test_prompts.json          (12 prompts NEVER seen during training)
        data/finetuned_deployment_name.txt        (produced by Exercise 6)

Writes  data/comparison_results.json              (side-by-side transcript)

Prints a compact table so the student can eyeball which model correctly:
  1. Names Summitline SKUs (pattern NW-SL-###) instead of off-brand recommendations.
  2. Cites the tool it used (get_weather / calculate / lookup_inventory / gear_match).
  3. Stays in the concierge tone (one or two sentences, friendly, concise).

Run:
    python src/compare_base_vs_finetuned.py
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI


REPO_ROOT = Path(__file__).resolve().parent.parent
TEST_PROMPTS = REPO_ROOT / "data" / "held_out_test_prompts.json"
FINETUNED_DEPLOYMENT_NAME = REPO_ROOT / "data" / "finetuned_deployment_name.txt"
COMPARISON_RESULTS = REPO_ROOT / "data" / "comparison_results.json"

# The concierge system prompt is intentionally NOT passed to the fine-tuned model
# on inference — the fine-tune should have absorbed the persona. Only the base
# model receives the explicit persona instructions, which gives us an
# apples-to-apples read on whether fine-tuning worked.
BASE_SYSTEM = (
    "You are the Summitline Outfitters gear concierge, a helpful assistant for a specialty "
    "outdoor-gear retailer covering hiking, climbing, and backcountry gear. Recommend real "
    "in-catalog Summitline SKUs (pattern NW-SL-###). Cite the tool you used (get_weather, "
    "calculate, lookup_inventory, gear_match) in one short sentence. Keep replies concise "
    "and friendly — one or two sentences."
)
FINETUNED_SYSTEM = BASE_SYSTEM  # Both models see the same system prompt for fairness.

SKU_PATTERN = re.compile(r"NW-SL-\d{3}")
TOOL_PATTERN = re.compile(r"\b(get_weather|calculate|lookup_inventory|gear_match)\b")


def build_client() -> AzureOpenAI:
    load_dotenv()
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(),
        "https://cognitiveservices.azure.com/.default",
    )
    return AzureOpenAI(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        azure_ad_token_provider=token_provider,
        api_version="2024-10-21",
    )


def ask(client: AzureOpenAI, deployment: str, system: str, user: str) -> str:
    """Return the assistant's reply text for a single-turn chat completion.

    TODO (Exercise 7 Step 2):
        Call client.chat.completions.create(
            model=deployment,
            messages=[{"role":"system","content":system}, {"role":"user","content":user}],
            max_completion_tokens=180,
            temperature=0.2,
        )
        Return the assistant reply text (choices[0].message.content).
    """
    # ---- Exercise 7 Step 2 Start ----
    raise NotImplementedError("Implement ask() — Exercise 7 Step 2")
    # ---- Exercise 7 Step 2 End ----


def score(reply: str) -> Dict[str, bool]:
    """Simple heuristic scorer used by Exercise 7 Step 3."""
    return {
        "names_summitline_sku": bool(SKU_PATTERN.search(reply)),
        "cites_a_tool": bool(TOOL_PATTERN.search(reply)),
        "two_sentences_or_less": reply.count(".") <= 2,
    }


def main() -> int:
    if not FINETUNED_DEPLOYMENT_NAME.exists():
        print(
            f"ERROR: {FINETUNED_DEPLOYMENT_NAME} not found — run src/deploy_finetuned.py first.",
            file=sys.stderr,
        )
        return 1
    finetuned_deployment = FINETUNED_DEPLOYMENT_NAME.read_text(encoding="utf-8").strip()
    base_deployment = os.environ["BASE_MODEL_DEPLOYMENT"]

    prompts: List[str] = json.loads(TEST_PROMPTS.read_text(encoding="utf-8"))["prompts"]
    client = build_client()

    results = []
    for i, user_prompt in enumerate(prompts, start=1):
        base_reply = ask(client, base_deployment, BASE_SYSTEM, user_prompt)
        ft_reply = ask(client, finetuned_deployment, FINETUNED_SYSTEM, user_prompt)
        row = {
            "index": i,
            "prompt": user_prompt,
            "base_reply": base_reply,
            "finetuned_reply": ft_reply,
            "base_score": score(base_reply),
            "finetuned_score": score(ft_reply),
        }
        results.append(row)
        print(f"\n[{i:>2}] {user_prompt}")
        print(f"     BASE:      {base_reply}")
        print(f"     FINETUNED: {ft_reply}")

    COMPARISON_RESULTS.write_text(json.dumps(results, indent=2), encoding="utf-8")

    base_sku = sum(r["base_score"]["names_summitline_sku"] for r in results)
    ft_sku = sum(r["finetuned_score"]["names_summitline_sku"] for r in results)
    base_tool = sum(r["base_score"]["cites_a_tool"] for r in results)
    ft_tool = sum(r["finetuned_score"]["cites_a_tool"] for r in results)
    total = len(results)
    print("\n--- Summary ---")
    print(f"Names a Summitline SKU:  base {base_sku}/{total}  |  fine-tuned {ft_sku}/{total}")
    print(f"Cites a tool:            base {base_tool}/{total}  |  fine-tuned {ft_tool}/{total}")
    print(f"\nFull transcript: {COMPARISON_RESULTS}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
