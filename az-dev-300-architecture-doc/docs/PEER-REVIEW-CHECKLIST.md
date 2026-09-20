# TaskForge Architecture — Peer-Review Checklist

Run this against your own doc BEFORE requesting stakeholder review.

## Diagrams
- [ ] Context view has TaskForge as ONE box (not decomposed)
- [ ] Context view shows all external actors + external systems with labeled arrows
- [ ] Container view decomposes into deployable units only
- [ ] Component view zooms into ONE interesting container (usually the Blazor app)
- [ ] Every service appearing in a diagram appears in the service-selection matrix (traceability)

## Service matrix
- [ ] Every row has a "why-not-alternative" cell
- [ ] Every row has a "cost note" cell with a $/month at 10k tenants
- [ ] Every row has a "risk" cell

## Cost model
- [ ] Per-service line items with source assumptions
- [ ] Traffic + tenant assumptions cited in the same doc
- [ ] Top 3-4 dominant line items called out
- [ ] Levers if the budget is halved (per line item)

## Risk log
- [ ] At least: data leak, region failure, cost overrun, partner-integration break
- [ ] Each row has likelihood × impact + mitigation
