"""
Extract receipt fields from an image using Azure Content Understanding.
"""
from pathlib import Path

from analyzer import create_or_update_analyzer, load_schema, poll_result, submit_content

ANALYZER_ID = "ai901-receipt"
HERE = Path(__file__).parent
SCHEMA = HERE / "schemas" / "receipt.json"
SAMPLE = HERE / "sample_data" / "receipt.jpg"


def main() -> None:
    create_or_update_analyzer(ANALYZER_ID, load_schema(SCHEMA))
    op_url = submit_content(ANALYZER_ID, SAMPLE, content_type="image/jpeg")
    result = poll_result(op_url)
    # TODO 1: print merchant_name, total, date, and each line item.
    raise NotImplementedError


if __name__ == "__main__":
    main()
