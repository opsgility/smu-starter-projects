"""
Run the full text-analysis pipeline across every review in sample_data/reviews.txt.

For each review print:
- Overall sentiment (Language SDK)
- Key phrases (Language SDK)
- Named entities (Language SDK)
- One-sentence summary (Foundry chat model)
"""
from pathlib import Path

from language_calls import analyze_entities, analyze_key_phrases, analyze_sentiment
from summarize import summarize_one

HERE = Path(__file__).parent
REVIEWS = (HERE / "sample_data" / "reviews.txt").read_text(encoding="utf-8").splitlines()


def main() -> None:
    reviews = [r.strip() for r in REVIEWS if r.strip()]

    # TODO 1: call analyze_sentiment(reviews) and store results.
    # TODO 2: call analyze_key_phrases(reviews) and store results.
    # TODO 3: call analyze_entities(reviews) and store results.
    # TODO 4: for each review, call summarize_one(review) for the generative summary.
    # TODO 5: pretty-print the combined output per review.
    raise NotImplementedError


if __name__ == "__main__":
    main()
