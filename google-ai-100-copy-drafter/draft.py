"""
Google AI 100 — Lesson 5: Policy-Aware Copy Drafter.

Generates on-brand, policy-compliant catalog copy for a Nimbus product.
"""
import json
import os
from pathlib import Path
from typing import List

import typer
from google import genai
from google.genai.types import GenerateContentConfig
from pydantic import BaseModel, Field
from rich.console import Console

app = typer.Typer(add_completion=False)
console = Console()

PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")


class CatalogCopy(BaseModel):
    headline: str = Field(description="<= 8 words")
    subhead: str = Field(description="One sentence, <= 20 words")
    body: str = Field(description="2-3 sentences of product copy")
    cta: str = Field(description="Call to action, <= 5 words")


def build_system(tone_path: Path, policy_path: Path) -> str:
    tone = tone_path.read_text(encoding="utf-8")
    policy = policy_path.read_text(encoding="utf-8")
    return (
        "You are a Nimbus Outfitters copywriter. Obey tone of voice and content "
        "policy exactly.\n\n"
        f"## Tone of voice\n{tone}\n\n## Content policy\n{policy}"
    )


@app.command()
def run(
    product: str = typer.Argument(..., help="Product name to write copy for"),
    features: List[str] = typer.Option([], "--feature", "-f", help="Repeatable"),
    model: str = typer.Option("gemini-2.5-flash", "--model"),
    structured: bool = typer.Option(False, "--structured/--no-structured"),
    thinking_budget: int = typer.Option(0, "--thinking-budget", help="0 disables thinking"),
) -> None:
    if not PROJECT:
        raise SystemExit("GOOGLE_CLOUD_PROJECT is not set.")

    client = genai.Client(vertexai=True, project=PROJECT, location=LOCATION)
    system = build_system(Path("tone_of_voice.md"), Path("content_policy.md"))
    prompt = f"Write catalog copy for the Nimbus {product}. Features: {', '.join(features) or 'general outdoor use'}."

    # TODO (Part 1): pass system_instruction=system via GenerateContentConfig, temperature=0.4
    # TODO (Part 2): when --structured, set response_mime_type="application/json",
    #   response_schema=CatalogCopy. Print parsed JSON.
    # TODO (Part 3): flip one safety threshold to BLOCK_LOW_AND_ABOVE and prove a block.
    # TODO (Part 4): if --thinking-budget > 0 and model is Pro/3.x, enable thinking.

    console.print("[yellow]Not implemented yet — complete the TODOs.[/]")


if __name__ == "__main__":
    app()
