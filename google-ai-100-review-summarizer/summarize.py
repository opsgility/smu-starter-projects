"""
Google AI 100 — Lesson 3: Review-Summarizer CLI.

Read reviews.csv, summarize each with Gemini on Vertex AI, and write
summaries.jsonl. Supports streaming output and a --model flag.
"""
import csv
import json
import os
import sys
import time
from pathlib import Path

import typer
from google import genai
from google.genai.types import GenerateContentConfig
from rich.console import Console

app = typer.Typer(add_completion=False)
console = Console()

PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

SYSTEM = (
    "Summarize the review in ONE SENTENCE. Mention the single strongest pro and "
    "the single strongest con if the reviewer gave one. Do not invent details."
)


def get_client() -> genai.Client:
    if not PROJECT:
        raise SystemExit("GOOGLE_CLOUD_PROJECT is not set.")
    return genai.Client(vertexai=True, project=PROJECT, location=LOCATION)


@app.command()
def run(
    input_path: Path = typer.Option(Path("reviews.csv"), "--input"),
    output_path: Path = typer.Option(Path("summaries.jsonl"), "--output"),
    model: str = typer.Option("gemini-2.5-flash", "--model"),
    stream: bool = typer.Option(False, "--stream/--no-stream"),
    limit: int = typer.Option(20, "--limit"),
) -> None:
    """Summarize reviews with Gemini on Vertex AI."""
    client = get_client()
    config = GenerateContentConfig(system_instruction=SYSTEM, temperature=0.2)

    total_in = total_out = 0
    start = time.time()

    with input_path.open(encoding="utf-8") as fin, output_path.open("w", encoding="utf-8") as fout:
        reader = csv.DictReader(fin)
        for i, row in enumerate(reader):
            if i >= limit:
                break
            product = row["product"]
            review_text = row["review_text"]
            console.rule(f"[bold]{i + 1}. {product}")

            # TODO (Part 1): single-call, print response.text
            # TODO (Part 2): switch to streaming via client.models.generate_content_stream
            # TODO (Part 3): record input+output tokens and write a JSON line
            summary = "<not implemented>"

            fout.write(json.dumps({"product": product, "summary": summary}) + "\n")

    elapsed = time.time() - start
    console.print(
        f"\n[bold green]Done[/] — {limit} reviews in {elapsed:.1f}s, "
        f"model={model}, tokens in/out={total_in}/{total_out}"
    )


if __name__ == "__main__":
    app()
