"""
Use Azure AI Vision ImageAnalysisClient to extract captions, tags, and objects
from a local image.
"""
import os
import sys
from pathlib import Path

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ["VISION_ENDPOINT"]
KEY = os.environ["VISION_KEY"]
HERE = Path(__file__).parent


def analyze(path: Path) -> dict:
    client = ImageAnalysisClient(endpoint=ENDPOINT, credential=AzureKeyCredential(KEY))

    # TODO 1: call client.analyze(
    #             image_data=path.read_bytes(),
    #             visual_features=[VisualFeatures.CAPTION, VisualFeatures.TAGS, VisualFeatures.OBJECTS],
    #         )
    # TODO 2: build a dict with:
    #           caption.text, caption.confidence,
    #           tags = [t.name for t in tags.list],
    #           objects = [{name, confidence} for each object]
    raise NotImplementedError


if __name__ == "__main__":
    img = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "sample_data" / "storefront.jpg"
    print(analyze(img))
