# Products API — contract notes

This file captures the OpenAPI 3.1 contract commitments Halcyon has made to downstream consumers of `Halcyon.Adventure.Api`. The generated contract lives at `/openapi/v1.yaml`.

## Consumers

- **Halcyon.Adventure.SalesPortal** (Course 5) — reads product catalogue, drives order-entry forms off the DTO shape.
- **Halcyon.Adventure.Etl** (Course 8) — reads product deltas on a schedule.

Both projects generate clients from the committed contract. A breaking shape change here is a breaking change everywhere.

## Versioning policy

- The contract is served under API version `1.0`.
- URL form: `/api/v1/products`.
- Header form: `/api/products` with `Api-Version: 1.0`.
- Default version when neither is supplied is `1.0`.

## Open items from the Lesson 2 PR review

Christopher's comment on PR #1 (merged):

> Nice ship. The POST /products endpoint comes back with a bare `400 Bad Request` and no body when I send `{}`. Fix before external consumers see this — they will not know what field they got wrong. The team standard is RFC 7807 problem-details with a trace id in `traceId`.

This is the Lesson 4 scope.

## Lesson 4 scope

- Add DataAnnotations to `CreateProductRequest` and `UpdateProductRequest`.
- Add one `IValidatableObject` cross-field rule — Halcyon's margin policy says `ListPrice` must be at least `1.2 × StandardCost`.
- Register `AddValidation()` so the built-in minimal-API validation filter runs on every endpoint.
- Register a custom `IProblemDetailsService` that includes a `traceId` extension on every problem-details response.
- Add one FluentValidation endpoint as a comparison so the decision between built-in and FluentValidation lands in `.github/copilot-instructions.md`.

Everything is deliberately absent in this starter so Lesson 4 can land it with Copilot Edits.
