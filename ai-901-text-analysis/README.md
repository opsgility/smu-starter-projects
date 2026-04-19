# ai-901-text-analysis — Azure AI Language scaffold

Starter for AI-901 Obj 2 Part IV (Text Analysis with Foundry). Four empty analysis functions and a small corpus of product reviews. The exercise has you implement:

1. `extract_key_phrases(text)` via `TextAnalyticsClient.extract_key_phrases`
2. `recognize_entities(text)` via `recognize_entities`
3. `analyze_sentiment(text)` via `analyze_sentiment`
4. `summarize_text(text)` via `extractive_summarize` (or `abstractive_summarize`)

## What's here
- `src/analyze.py` — four stubs, each raising `NotImplementedError`. `main()` iterates over `sample_data/reviews.txt` and tries to call each function.
- `sample_data/reviews.txt` — 5 product reviews of varying sentiment.

## Env vars
Copy `.env.example` → `.env` and set `LANGUAGE_ENDPOINT`.

## Run
```
python src/analyze.py
```
(First run prints NotImplementedError — implementing the four functions is the exercise.)
