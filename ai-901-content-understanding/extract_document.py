"""
Extract invoice fields from a PDF using Azure Content Understanding.
"""
from pathlib import Path

from analyzer import (
    create_or_update_analyzer,
    load_schema,
    poll_result,
    submit_content,
)

ANALYZER_ID = "ai901-invoice"
HERE = Path(__file__).parent
SCHEMA = HERE / "schemas" / "invoice.json"
SAMPLE = HERE / "sample_data" / "invoice.pdf"


def main() -> None:
    create_or_update_analyzer(ANALYZER_ID, load_schema(SCHEMA))
    op_url = submit_content(ANALYZER_ID, SAMPLE, content_type="application/pdf")
    result = poll_result(op_url)
    # TODO 1: print the extracted fields from result['result']['contents'][0]['fields']
    raise NotImplementedError


if __name__ == "__main__":
    main()
