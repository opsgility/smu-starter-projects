# SIB Public Threat Indicator Feed — Overview

The **SIB Public Indicator Feed v3** is the bureau's curated stream of
unclassified, open-source threat indicators. The Concierge is
authorized to look up entries from this feed by indicator id.

## Indicator id format

`OSINT-IND-YYYY-NNNN`

- `YYYY`: four-digit year the indicator was first observed.
- `NNNN`: four-digit sequence number, zero-padded, monotonically
  increasing inside a year.

Examples:

- `OSINT-IND-2024-1042` — disinformation campaign tracker entry.
- `OSINT-IND-2024-1107` — public phishing kit reuse.
- `OSINT-IND-2024-1183` — maritime spoofing pattern.

## Entry fields

Every feed entry exposes the following fields. These are also what the
Concierge's `_indicator_status` tool returns:

- `indicator_id` — the canonical id above.
- `status` — one of `active`, `monitored`, `retired`.
- `feed` — always `SIB Public Indicator Feed v3` for entries from this
  feed.
- `last_observed` — ISO-8601 date of the most recent open-source
  sighting.

## Promotion vs publication

The Concierge can surface a feed entry's *attributes*. It cannot
*promote* an entry from collection into a publication; promotion goes
through the editorial pipeline described in `publication-policy.md`.
