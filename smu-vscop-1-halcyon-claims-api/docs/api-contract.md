# Halcyon Claims API — contract

Base URL (dev): `http://localhost:5000`

## /api/policies

### GET /api/policies

Returns all policies. Status: `200 OK`. Body: array of `Policy`.

### GET /api/policies/{id}

Returns one policy by numeric id. Status: `200 OK` or `404 Not Found`.

### POST /api/policies

Creates a new policy. Body: `Policy` (Id ignored on input). Status: `201 Created` with `Location: /api/policies/{id}` header. `400 Bad Request` with a `reason` string if the policy number does not match the `POL-NNNNNNN` format.

## /api/claims

### GET /api/claims

Returns all claims. Status: `200 OK`. Body: array of `Claim`.

### GET /api/claims/{id}

Returns one claim by numeric id. Status: `200 OK` or `404 Not Found`.

### POST /api/claims

Submits a new claim. Body: `Claim` (Id ignored on input, Status defaulted to `"Submitted"`). The server:

1. Validates the policy number format (`POL-NNNNNNN`).
2. Looks up the policy by number.
3. Runs `IClaimValidationService.ValidateClaimAsync` — rejects on inactive policy, expired dates, over-coverage amount, or duplicate claim.

Status: `201 Created` on success. `400 Bad Request` with a `reason` string on any validation failure.

## Shared types

### Policy

```
{
  "id": 1,
  "policyNumber": "POL-0000001",
  "holder": "Jordan Avery",
  "coverageAmount": 150000.00,
  "effectiveDate": "2025-12-02T00:00:00Z",
  "expirationDate": "2026-12-02T00:00:00Z",
  "isActive": true
}
```

### Claim

```
{
  "id": 1,
  "policyNumber": "POL-0000001",
  "claimAmount": 850.00,
  "incidentDate": "2026-09-18T00:00:00Z",
  "description": "Water damage to kitchen flooring.",
  "status": "Approved"
}
```

## Error shape

Non-200 responses carry a plain-text or JSON `reason`:

```
400 Bad Request
Content-Type: text/plain
"Invalid policy number format. Expected POL- followed by 7 digits."
```

Status codes used: `200`, `201`, `400`, `404`. The service does not currently emit `401` or `403` — auth is enforced at the Front Door edge in production.
