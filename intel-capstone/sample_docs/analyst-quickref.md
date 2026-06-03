# SIB OSINT Concierge — Analyst Quick Reference

The five tasks the Concierge sees most often, with the recommended
analyst phrasing.

## 1. Summarize public reporting on a topic

> "Summarize the latest public reporting on `<topic-slug>`."

The Concierge will pull the most recent entry for that topic from the
open-source news cache and return a short, source-cited summary.

## 2. Look up an indicator

> "Look up indicator `OSINT-IND-2024-1042`."

The Concierge calls its `_indicator_status` tool and returns
`indicator_id`, `status`, `feed`, and `last_observed`. To see narrative
attributes, follow up with "and explain it" — the Concierge will then
retrieve the matching entry from the KB.

## 3. Draft a candidate paragraph for the Daily Summary

> "Draft a Daily Summary paragraph on `<topic-slug>`."

The Concierge returns a candidate paragraph watermarked
`DRAFT — NOT FOR PUBLICATION`, valid for 24 hours.

## 4. Quick analyst math

> "What is the percent change from 4,200 to 4,820?"

The Concierge uses its `calculate` tool. Results round to two decimal
places by default.

## 5. Handbook / policy lookup

> "What's the retention window for raw collection material?"

The Concierge calls the RAG endpoint, retrieves the relevant policy
chunk, and answers with a `[source.md]` citation. Always inspect the
cited file before quoting in a product.
