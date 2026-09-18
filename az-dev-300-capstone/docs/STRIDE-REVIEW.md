# TaskForge STRIDE-lite security review

## Spoofing
- **Threat:** attacker impersonates a tenant user
- **Mitigations:** Entra External ID auth; APIM validate-jwt at edge; backend re-validates via Microsoft.Identity.Web

## Tampering
- **Threat:** data modified in transit or at rest
- **Mitigations:** TLS 1.2+ everywhere; Cosmos + SQL encryption at rest by default; secrets in Key Vault + App Configuration; audit event on every state change

## Repudiation
- **Threat:** user denies an action
- **Mitigations:** `AuditEvents` table with actorOid + timestamp; App Insights request logs; RecordAssessment audit trail

## Information disclosure (I) — HIGHEST PRIORITY for TaskForge
- **Threat:** cross-tenant data leak
- **Mitigations:** Row-Level Security with FILTER + BLOCK predicates; hierarchical partition key `/tenantId/projectId`; JWT `tid` claim enforcement at APIM + backend
- **Ongoing:** quarterly RLS penetration test

## Denial of service
- **Threat:** one tenant floods the platform
- **Mitigations:** APIM `<rate-limit-by-key>` per subscription; Front Door WAF; App Service autoscale rules; SB DLQ + retry policies

## Elevation of privilege
- **Threat:** tenant escalates to platform-admin
- **Mitigations:** two-identity separation (External ID vs Workforce Entra); admin app validates only Workforce issuer; `[Authorize(Roles="TaskForge.Admin")]` on every admin page
