"""
Google AI 100 — Lesson 4: Product-Photo Describer.

Given a list of GCS image URIs, ask Gemini to describe each photo. Supports
structured JSON output via response_schema.
"""
import json
import os
from pathlib import Path

import typer
from google import genai
from google.genai.types import (
    Content,
    GenerateContentConfig,
    Part,
)
from rich.console import Console

app = typer.Typer(add_completion=False)
console = Console()

PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

SYSTEM = (
    "You are a product merchandiser for Nimbus Outfitters. When given a product "
    "photo, describe it accurately and briefly. Never invent details not visible."
)


def get_client() -> genai.Client:
    if not PROJECT:
        raise SystemExit("GOOGLE_CLOUD_PROJECT is not set.")
    return genai.Client(vertexai=True, project=PROJECT, location=LOCATION)


@app.command()
def run(
    photos_path: Path = typer.Option(Path("photos.json"), "--photos"),
    output_path: Path = typer.Option(Path("catalog.jsonl"), "--output"),
    model: str = typer.Option("gemini-3.1-flash", "--model"),
    structured: bool = typer.Option(False, "--structured/--no-structured"),
) -> None:
    """Describe each photo referenced by a gs:// URI in photos.json."""
    client = get_client()
    photos = json.loads(photos_path.read_text(encoding="utf-8"))
    if not photos:
        console.print("[red]photos.json is empty — follow README prep step.[/]")
        raise SystemExit(1)

    with output_path.open("w", encoding="utf-8") as fout:
        for gs_uri in photos:
            console.rule(gs_uri)

            # TODO (Part 1): build contents with Part.from_uri(file_uri=gs_uri, mime_type="image/jpeg")
            #   then a text Part "Describe this product in 2 sentences."
            #   call client.models.generate_content and print response.text

            # TODO (Part 2): when --structured is set, pass response_mime_type="application/json"
            #   with a response_schema requiring:
            #   { product_type, primary_color, materials[], one_line_marketing_copy }

            record = {"uri": gs_uri, "description": "<not implemented>"}
            fout.write(json.dumps(record) + "\n")


if __name__ == "__main__":
    app()
