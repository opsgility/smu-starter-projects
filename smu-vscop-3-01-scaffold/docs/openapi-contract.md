# Products API — Contract draft

**Author:** Christopher Jones (Engineering Director, Halcyon Insurance)
**Draft date:** Sprint 2026-Q4-S1 kickoff
**Owner for build:** Dana Reyes
**Target service:** `Halcyon.Adventure.Api`
**Backing data:** `AdventureWorks2025.Production.Product` (shared VM-local SQL Server, Windows integrated auth)

Dana — this is the shape I need by end of quarter. The Sales Portal team (course 5 downstream) and the Analytics Dashboard team (course 6 downstream) are both planning around this contract. Treat the field names as frozen; everything else is Ask-mode fodder. — Christopher

---

## Endpoints

| Verb | Route | Purpose |
| --- | --- | --- |
| GET | `/api/v1/products` | List products with pagination (`page`, `pageSize`), optional `nameContains` filter. |
| GET | `/api/v1/products/{id}` | Return a single product by `ProductID`. |
| POST | `/api/v1/products` | Create a product (admins only — auth lands in course 5). |
| PUT | `/api/v1/products/{id}` | Update a product. Optimistic concurrency via `rowversion`. |
| DELETE | `/api/v1/products/{id}` | Soft-delete (set `DiscontinuedDate` to today — never physical delete). |

Dual versioning: URL segment (`/api/v1/...`) **and** `X-Api-Version: 1.0` header. Both resolve to the same controller — the versioning library picks whichever the client sent. Lesson 2 adds URL versioning first, header versioning last.

## Request / response shapes

### Product resource (response)

```json
{
  "productId": 707,
  "name": "Sport-100 Helmet, Red",
  "productNumber": "HL-U509-R",
  "color": "Red",
  "safetyStockLevel": 4,
  "reorderPoint": 3,
  "standardCost": 13.0863,
  "listPrice": 34.99,
  "size": null,
  "weight": null,
  "productLine": "R",
  "sellStartDate": "2003-07-01T00:00:00",
  "sellEndDate": null,
  "discontinuedDate": null,
  "rowVersion": "AAAAAAAAB9E="
}
```

### Create / update request

```json
{
  "name": "Sport-100 Helmet, Red",
  "productNumber": "HL-U509-R",
  "color": "Red",
  "safetyStockLevel": 4,
  "reorderPoint": 3,
  "standardCost": 13.0863,
  "listPrice": 34.99,
  "productLine": "R",
  "sellStartDate": "2026-11-01T00:00:00"
}
```

### Error response

RFC 7807 problem-details — same shape across every endpoint. Lesson 4 (validation lab) hardens this surface; for the Lesson 2 build, the ASP.NET Core default problem-details response is fine.

```json
{
  "type": "https://halcyon-adventure.example/errors/not-found",
  "title": "Product not found",
  "status": 404,
  "detail": "No product exists with ProductID 999999.",
  "traceId": "00-7a3b4c5d6e-00"
}
```

## Behaviour rules

1. `GET /api/v1/products` defaults to `page=1`, `pageSize=25`. Max `pageSize=100`; anything over returns `400`.
2. `GET /api/v1/products/{id}` returns `404` when the product does not exist (not `204`, not an empty `200`).
3. `POST` returns `201 Created` with a `Location` header pointing at the new resource.
4. `PUT` returns `204 No Content` on success, `409 Conflict` on a `rowversion` mismatch.
5. `DELETE` is a soft-delete — set `DiscontinuedDate` to today; subsequent `GET` by id returns `410 Gone`. Marcus's team at Halcyon will not accept physical deletes on acquired-system data.
6. Every response uses `TypedResults` on the server side (not the untyped `Results` factory) so the OpenAPI document can describe the response shape without extra annotations.

## OpenAPI document

Serve the generated document at `/openapi/v1.yaml` (YAML, not JSON — Christopher's architecture review tooling reads YAML). The document MUST advertise OpenAPI 3.1 — the Sales Portal client generator in course 5 depends on 3.1 schema features.

## Deferred (not in this lab)

- Authentication / authorization — course 5 adds Entra ID.
- Validation beyond "field is required" — lesson 4 lands DataAnnotations + `IValidatableObject` + `IProblemDetailsService`.
- Correlation IDs, structured logging, rate limiting — lesson 6 covers these.
- Caching, ETags — out of scope for the Course 3 arc entirely.

## Review notes

Lesson 1's Ask-mode exercise walks Dana through reviewing this document with Copilot before building against it. Expected questions a careful review surfaces: the missing `rowversion` on the create request, whether `productId` should appear in the create body (it should not — SQL Server IDENTITY column assigns it), and whether `409` on PUT should include the current server state (Christopher's call: no, keep the response small; a client that cares re-fetches).
