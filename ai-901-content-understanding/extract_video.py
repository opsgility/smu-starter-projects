"""
Extract information from a short video (MP4) using Azure Content Understanding.
"""
from pathlib import Path

from analyzer import create_or_update_analyzer, load_schema, poll_result, submit_content

ANALYZER_ID = "ai901-training-video"
HERE = Path(__file__).parent
SCHEMA = HERE / "schemas" / "training_video.json"
SAMPLE = HERE / "sample_data" / "training.mp4"


def main() -> None:
    create_or_update_analyzer(ANALYZER_ID, load_schema(SCHEMA))
    op_url = submit_content(ANALYZER_ID, SAMPLE, content_type="video/mp4")
    result = poll_result(op_url)
    # TODO 1: print the scene-by-scene topic list and any extracted learning objectives.
    raise NotImplementedError


if __name__ == "__main__":
    main()
