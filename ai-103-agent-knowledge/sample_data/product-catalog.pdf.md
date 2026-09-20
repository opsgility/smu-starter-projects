# product-catalog.pdf (placeholder)

**This markdown file is a stand-in.** The actual file the exercises upload
is `sample_data/product-catalog.pdf`. The lab environment seeds that PDF
before the learner starts. If for any reason it is missing, drop in any
small PDF whose text content mentions a few product entries and re-run
`python -m app.agent`.

## Expected content

A short product catalog for Summitline Outfitters covering at least three
of the following lines so the FileSearchTool has something to ground on:

- **Alpine 4S tent** — 4-season, 4.6 lbs, double-wall, $649
- **Ridgeline daypack** — 28L, hydration-compatible, $129
- **Cascade 600 sleeping bag** — 15 degF, 800-fill down, $299
- **Summit 30L rain shell** — 3-layer waterproof, $189
- **Trailhead insulated flask** — 24 oz, double-wall, $45

The concierge agent should be able to answer "What products do we sell?"
and "Do you carry a 4-season tent under 5 lbs?" using this catalog.
