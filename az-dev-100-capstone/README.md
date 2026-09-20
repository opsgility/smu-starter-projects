# AZ-DEV-100 M10L20 — Anchorline Capstone

Starter for the AZ-DEV-100 capstone. Everything from Modules 1–9 is already wired:

- ASP.NET Core minimal-API (.NET 10)
- `Azure.Monitor.OpenTelemetry.AspNetCore` **already registered** — the capstone assumes OTel is on
- Meter `Anchorline.Storefront` with `anchorline.checkout.requests` counter + `anchorline.checkout.duration_ms` histogram
- `ActivitySource("Anchorline.Storefront")` with per-stage activities inside `/checkout`
- Endpoints: `/health`, `/version`, `/launch-tag`, `/fast`, `/slow`, `/checkout`, `/fail`

## Runtime configuration expected

App settings (pre-provisioned by the capstone ARM template on the parent app):

- `APPLICATIONINSIGHTS_CONNECTION_STRING` — Azure Monitor destination for OTel
- `AZ_DEV_100_BUILD_TAG` — surfaced by `/version`
- `Anchorline__LaunchTag` — Key Vault reference to `AnchorlineLaunchTag` secret; surfaced by `/launch-tag`

## Scripts

- `scripts/load.sh <host> [duration] [rps]` — mixed load generator (fast/slow/checkout/fail). Effective rate is ~75% of the nominal RPS because of the inter-batch `sleep 1`.
- `scripts/bad-checkout.patch` — git diff introducing the deliberate `/checkout` bug for Exercise 4. Apply with `git apply scripts/bad-checkout.patch` (or edit `Program.cs` by hand per the exercise).
