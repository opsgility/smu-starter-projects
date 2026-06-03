# SIB OSINT Concierge — Collection Policy

The Concierge is permitted to retrieve from a defined set of **public,
non-classified** open-source data sources. Any source not on this list
must be reviewed by the OSINT Modernization team before it can be added
to the Concierge index.

## In-scope sources

- Public newswire and broadcast transcripts that the bureau has a
  redistribution license for.
- Public threat-intelligence feeds the bureau subscribes to (e.g.
  open-source phishing kits, public IOC lists, public AIS data).
- Public government statements, treaty texts, and UN reporting.
- Public academic and think-tank publications under standard fair-use
  citation.

## Out-of-scope sources

- Anything classified at Confidential or higher.
- Scraped social-media content from platforms whose terms of service
  prohibit automated retrieval.
- Personally identifiable information about private individuals.

## Retention

The Concierge keeps raw collection material for **180 days** in the
collection store, after which it is purged unless a flagged piece of
material has been promoted to an active product.

Embeddings of retained material live in the Azure AI Search index and
are re-built monthly. Re-builds use the same retention window — content
removed from collection is removed from the index on the next rebuild.

## Source filenames

Every retrieved chunk in a Concierge response is cited with the source
filename in square brackets, for example `[collection-policy.md]`. The
filename always resolves to the canonical document in the bureau's
unclassified knowledge base.
