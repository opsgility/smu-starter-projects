# Halcyon.Adventure.Api — OpenAPI contract notes

The OpenAPI 3.1 document is generated at request time by `Microsoft.AspNetCore.OpenApi`.
In Development it is served at `/openapi/v1.json`. Two versions ship:

| Version | Base path | Reader | Shape delta vs v1 |
| --- | --- | --- | --- |
| `v1` | `/v1/products` | URL segment OR `X-Api-Version: 1.0` | — |
| `v2` | `/v2/products` | URL segment OR `X-Api-Version: 2.0` | Reserved for the Lesson 2 follow-up; shape currently matches v1. |

## Error envelope

Every 4xx and 5xx response flows through the custom `HalcyonProblemDetailsService`
and ships as RFC 9457 `application/problem+json` with these extensions:

- `traceId` — W3C trace parent, or `HttpContext.TraceIdentifier` as a fallback.
- `halcyonCorrelationId` — mirrors the `X-Correlation-Id` request header
  (populated once Lesson 6's correlation middleware lands).
- `type` — `https://halcyon.example.com/problems/{status}` by default; endpoints
  can override by setting `ProblemDetails.Type` before the writer runs.

## Validation surface

- Built-in: `AddValidation()` + DataAnnotations + one `IValidatableObject`
  cross-field rule enforcing the price-vs-cost margin.
- Comparison: `POST /v1/products/create-with-fluent-validation` uses
  FluentValidation. Same shape, same rules — kept so Lesson 3's Edit-mode walk
  can diff the two paths.
