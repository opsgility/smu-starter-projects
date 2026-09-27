"""Debate + synthesis pattern."""

import os, sys
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import anthropic


PERSPECTIVES = {
    "conservative": "You are a risk-averse advisor. Prioritize safety, delay, and thorough validation.",
    "aggressive":   "You are a growth-focused advisor. Prioritize speed, iteration, and market capture.",
    "contrarian":   "You are a contrarian. Argue the least-obvious answer; challenge conventional wisdom.",
}


def one_advisor(client, model, name: str, system_prompt: str, question: str) -> tuple[str, str]:
    resp = client.messages.create(model=model, max_tokens=400,
        system=system_prompt, messages=[{"role":"user","content": question}])
    text = next((b.text for b in resp.content if b.type == "text"), "")
    return (name, text)


def synthesize(client, model, question: str, advisor_answers: list[tuple[str, str]]) -> str:
    formatted = "\n\n".join(f"[{name}]:\n{ans}" for name, ans in advisor_answers)
    prompt = f"Question: {question}\n\nAdvisors:\n{formatted}\n\nSynthesize a balanced 5-sentence recommendation drawing on all three perspectives."
    resp = client.messages.create(model=model, max_tokens=500,
        messages=[{"role":"user","content": prompt}])
    return next((b.text for b in resp.content if b.type == "text"), "")


def main():
    load_dotenv()
    client = anthropic.Anthropic()
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")

    question = "Should Orion Analytics launch its new Fabric integration this quarter or wait until we have Enterprise SSO shipped?"
    print(f"QUESTION: {question}\n")

    # TODO: run each perspective in parallel via ThreadPoolExecutor.
    # HINT:
    #   with ThreadPoolExecutor(max_workers=3) as pool:
    #       results = list(pool.map(
    #           lambda kv: one_advisor(client, model, kv[0], kv[1], question),
    #           PERSPECTIVES.items()))
    try:
        results = None
        # ↑ replace with the ThreadPool call above
        raise NotImplementedError("TODO: parallel advisors")
    except NotImplementedError as e:
        print(f"TODO not filled: {e}"); return 1

    for name, ans in results:
        print(f"\n=== {name} ===\n{ans}")

    print("\n\n=== SYNTHESIS ===")
    print(synthesize(client, model, question, results))
    return 0


if __name__ == "__main__":
    sys.exit(main())
