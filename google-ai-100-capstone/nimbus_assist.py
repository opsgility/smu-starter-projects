"""
Google AI 100 — Capstone: nimbus-assist CLI.

Given a SKU, load its photo and spec PDF from GCS, then call Gemini on
Vertex AI to produce a CatalogEntry + one-sentence summary + 3 FAQ answers.

Outputs validated JSON matching schemas.AssistBundle.
"""
import json
import os
import time
from pathlib import Path

import typer
from google import genai
from google.genai.types import (
    Content,
    GenerateContentConfig,
    Part,
)
from rich.console import Console

from schemas import AssistBundle

app = typer.Typer(add_completion=False)
console = Console()

PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

SYSTEM = (
    "You are a Nimbus Outfitters merchandising assistant. Use only details you can\n"
    "see in the product photo or read in the spec PDF. Never fabricate materials,\n"
    "dimensions, prices, or certifications."
)


@app.command()
def run(
    sku: str = typer.Option(..., "--sku"),
    config_path: Path = typer.Option(Path("sku_config.json"), "--config"),
    model: str = typer.Option("gemini-2.5-flash", "--model"),
) -> None:
    if not PROJECT:
        raise SystemExit("GOOGLE_CLOUD_PROJECT is not set.")

    config = json.loads(config_path.read_text(encoding="utf-8"))
    entry = next((s for s in config["skus"] if s["sku"] == sku), None)
    if entry is None:
        raise SystemExit(f"Unknown SKU: {sku}")

    client = genai.Client(vertexai=True, project=PROJECT, location=LOCATION)

    # TODO: build multimodal contents = [Part.from_uri(photo, "image/jpeg"),
    #       Part.from_uri(spec, "application/pdf"), Part.from_text("instructions...")].
    # TODO: call client.models.generate_content with:
    #       config=GenerateContentConfig(
    #           system_instruction=SYSTEM,
    #           response_mime_type="application/json",
    #           response_schema=AssistBundle,
    #           temperature=0.3,
    #       )
    # TODO: parse response.text into AssistBundle, print indented JSON.
    # TODO: print usage_metadata (input, output, thoughts) and wall time.

    start = time.time()
    console.print(f"[yellow]Not implemented yet — complete TODOs for sku={sku}.[/]")
    console.print(f"Elapsed: {time.time() - start:.1f}s")


if __name__ == "__main__":
    app()
