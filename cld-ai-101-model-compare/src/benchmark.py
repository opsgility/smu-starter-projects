"""Exercise 1 — benchmark three Claude models on three prompts.

Runs the 3 x 3 matrix (three prompts x Haiku 4.5, Sonnet 5, Opus 5.5)
and writes a CSV of (prompt, model, input_tokens, output_tokens, latency_ms,
cost_usd, response_text) rows to results/.

Fable 5.1 is deliberately excluded — see README.md.

Run: `python src/benchmark.py`
"""

import csv
import os
import sys
import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
import anthropic

from pricing import compute_cost_usd


MODELS: list[str] = [
    "claude-haiku-4-5",
    "claude-sonnet-5",
    "claude-opus-5-5",
]

PROMPT_FILE = Path(__file__).resolve().parent.parent / "data" / "prompts.txt"
RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"


def load_prompts() -> list[str]:
    """Read the three test prompts from data/prompts.txt.

    Prompts are separated by lines starting with '===' — everything between
    two === markers (or a === marker and end-of-file) is one prompt. Blank
    lines and lines starting with '#' are ignored inside a prompt.
    """
    text = PROMPT_FILE.read_text(encoding="utf-8")
    prompts: list[str] = []
    current: list[str] = []
    for line in text.splitlines():
        if line.startswith("==="):
            if current:
                prompts.append("\n".join(current).strip())
                current = []
            continue
        if line.startswith("#"):
            continue
        current.append(line)
    if current:
        prompts.append("\n".join(current).strip())
    return [p for p in prompts if p]


def run_one(client: anthropic.Anthropic, model: str, prompt: str) -> dict:
    """Fire one request; return a row dict for the CSV."""
    t0 = time.perf_counter()
    response = client.messages.create(
        model=model,
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}],
    )
    latency_ms = int((time.perf_counter() - t0) * 1000)

    # response.content is a list of typed blocks. Adaptive-thinking models
    # (Opus 5.5 always, Fable 5.1 sometimes) may emit a ThinkingBlock
    # first — the actual reply lives in the text block. This benchmark
    # iterates all three tiers (Haiku 4.5 / Sonnet 5 / Opus 5.5), so
    # without this filter the loop crashes the moment it hits Opus.
    text = next((b.text for b in response.content if b.type == "text"), "")
    tokens_in = response.usage.input_tokens
    tokens_out = response.usage.output_tokens
    cost = compute_cost_usd(model, tokens_in, tokens_out)

    return {
        "prompt_first_50_chars": prompt[:50].replace("\n", " ") + ("…" if len(prompt) > 50 else ""),
        "model": model,
        "input_tokens": tokens_in,
        "output_tokens": tokens_out,
        "latency_ms": latency_ms,
        "cost_usd": cost,
        "response_text": text,
    }


def main() -> int:
    load_dotenv()
    client = anthropic.Anthropic()

    prompts = load_prompts()
    if len(prompts) != 3:
        print(
            f"benchmark: expected 3 prompts in {PROMPT_FILE}, found {len(prompts)}.",
            file=sys.stderr,
        )
        return 1

    print(f"benchmark: {len(prompts)} prompts x {len(MODELS)} models = "
          f"{len(prompts) * len(MODELS)} requests")

    rows: list[dict] = []
    for prompt_idx, prompt in enumerate(prompts, start=1):
        for model in MODELS:
            print(f"  [{prompt_idx}/{len(prompts)}] {model} ... ", end="", flush=True)
            try:
                row = run_one(client, model, prompt)
            except anthropic.APIError as e:
                print(f"ERROR ({e})")
                continue
            print(f"{row['latency_ms']} ms, {row['input_tokens']}+{row['output_tokens']} tok, "
                  f"${row['cost_usd']:.6f}")
            rows.append(row)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_path = RESULTS_DIR / f"benchmark-{ts}.csv"
    with out_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"\nbenchmark: wrote {len(rows)} rows to {out_path}")

    # TODO: extend this file for Exercise 3 — add an LLM-judge step that
    # sends the three model responses for each prompt to claude-sonnet-5
    # and asks which one is best (and why). Append the judge's verdict as
    # a new column in the CSV. Skeleton signature:
    #
    #   def judge(client, prompt, responses_by_model): -> {"best_model": ..., "rationale": ...}
    #
    # See README.md for the LLM-as-judge pattern this practices.
    return 0


if __name__ == "__main__":
    sys.exit(main())
