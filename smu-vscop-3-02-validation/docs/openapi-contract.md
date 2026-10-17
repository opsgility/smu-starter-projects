# Products API — contract notes

This file captures the OpenAPI 3.1 contract commitments Halcyon has made to downstream consumers of `Halcyon.Adventure.Api`. The generated contract lives at `/openapi/v1.yaml`.

## Consumers

- **Halcyon.Adventure.SalesPortal** (Course 5) — reads product catalogue, drives order-entry forms off the DTO shape.
- **Halcyon.Adventure.Etl** (Course 8) — reads product deltas on a schedule.

Both projects generate clients from the committed contract. A breaking shape change here is a breaking change everywhere.

## Request / response shapes (Lesson 4 scope)

### Create / update

```json
{
  "sku": "AW-HLM-001",
  "name": "Sport-100 Helmet, Red",
  "price": 34.99,
  "cost": 13.08
}
```

### Product resource (response)

```json
{
  "id": 1,
  "sku": "AW-HLM-001",
  "name": "Sport-100 Helmet, Red",
  "price": 34.99,
  "cost": 13.08
}
```

### Batch import

```json
{
  "items": [
    { "sku": "AW-X-1", "name": "Widget A", "price": 120.00, "cost": 100.00 },
    { "sku": "AW-X-2", "name": "Widget B", "price": 125.00, "cost": 100.00 }
  ]
}
```

## Open items from the Lesson 2 PR review

Christopher's comment on PR #1 (merged):

> Nice ship. The POST /products endpoint comes back with a bare `400 Bad Request` and no body when I send `{}`. Fix before external consumers see this — they will not know what field they got wrong. The team standard is RFC 7807 problem-details with a correlation / trace id on every error response.

## Lesson 4 scope

- Add DataAnnotations to `CreateProductRequest` and `UpdateProductRequest`.
- Add one `IValidatableObject` cross-field rule — Halcyon's margin policy says `Price >= 1.2 × Cost`.
- Register `AddValidation()` so the .NET 10 built-in minimal-API validation filter runs on every endpoint.
- Register `AddProblemDetails(options => options.CustomizeProblemDetails = ...)` so every problem-details response carries a `halcyonTraceId` extension sourced from `CorrelationIdMiddleware`.
- Introduce FluentValidation on exactly one endpoint — `POST /products/batch-import` — so the "built-in vs FluentValidation" decision lands in `.github/copilot-instructions.md`.

Everything in the Lesson 4 scope is deliberately absent in this starter so each Copilot Edits step lands it with a single prompt.
