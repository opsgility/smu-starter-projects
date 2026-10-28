# Halcyon Claims API — architecture

## About Halcyon Insurance

Halcyon Insurance is a mid-size US property & casualty carrier (~2,000 employees, HQ Hartford CT). SOC 2 Type II, state-regulated. The engineering org runs mostly .NET on Azure — a mix of modern ASP.NET Core microservices and WPF line-of-business apps on the broker and claims desks.

## About this service

The Halcyon Claims API is one of several ASP.NET Core services on the claims platform. It accepts new claim submissions, validates them against the underlying policy, and routes them through a triage pipeline. Downstream services pick up triage decisions and either auto-pay small approved claims or hand them to adjusters for review.

## Service shape

ASP.NET Core 8 Web API. Controllers at `/api/claims` and `/api/policies`. Services wired via DI in `Program.cs`:

- `IClaimValidationService` → `ClaimValidationService` — rejects claims against inactive, expired, or over-coverage policies; detects duplicate submissions.
- `IClaimTriageService` → `ClaimTriageService` — scores incoming valid claims against the policy's coverage ratio, flags fraud-watch patterns (claims submitted within 48h of policy start, frequent repeat claims).

Persistence is stubbed as in-memory lists in the controller and service classes for demo purposes. In production, both are backed by Azure SQL via EF Core and cached in Azure Cache for Redis.

## Deployment story

- **Dev / Test:** Azure App Service, F1 tier.
- **Production:** Azure Container Apps (east-us-2 + west-us-2), fronted by Azure Front Door with WAF.
- **CI/CD:** GitHub Actions builds + pushes to Azure Container Registry, deploys via `azd` to Container Apps revisions with blue/green cutover.
- **Observability:** OpenTelemetry OTLP export to Azure Application Insights. Dashboards in the "Claims Platform" App Insights workspace.

## Coding conventions

- Explicit nullable annotations enabled (`<Nullable>enable</Nullable>`).
- Services are internal interfaces + sealed implementation; test via the interface.
- Controllers thin; business logic in services.
- No business logic in `Program.cs`.
- No logging of PII; policy holder names and claim descriptions are redacted before being logged.
- All public API responses are JSON. 4xx responses carry a `reason` string, not a stack trace.
