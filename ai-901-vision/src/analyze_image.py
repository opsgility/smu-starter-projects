"""Azure AI Vision image analysis on a local file."""
from __future__ import annotations

import os
from pathlib import Path

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ.get("VISION_ENDPOINT")
SAMPLE = Path(__file__).parent.parent / "sample_data" / "retail_shelf.jpg"


def main() -> None:
    if not ENDPOINT:
        raise SystemExit("Set VISION_ENDPOINT in .env.")
    client = ImageAnalysisClient(endpoint=ENDPOINT, credential=DefaultAzureCredential())
    with SAMPLE.open("rb") as f:
        result = client.analyze(
            image_data=f.read(),
            visual_features=[
                VisualFeatures.CAPTION,
                VisualFeatures.TAGS,
                VisualFeatures.OBJECTS,
                VisualFeatures.READ,
            ],
            gender_neutral_caption=True,
        )
    if result.caption:
        print(f"caption: {result.caption.text} (conf={result.caption.confidence:.2f})")
    if result.tags:
        tags = [f"{t.name}({t.confidence:.2f})" for t in result.tags.list[:10]]
        print(f"tags: {', '.join(tags)}")
    if result.objects:
        for obj in result.objects.list:
            names = [t.name for t in obj.tags]
            print(f"object: {names}")
    if result.read and result.read.blocks:
        for block in result.read.blocks:
            for line in block.lines:
                print(f"ocr: {line.text}")


if __name__ == "__main__":
    main()
