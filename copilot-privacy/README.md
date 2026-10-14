# FleetBoard Privacy Starter

Starter for the GH-300 "Data Handling, Architecture and Privacy" hands-on lab.

The code in this folder is intentionally staged with example secrets and credentials inside `fleet-secrets/`, `credentials.json`, and `.env.fleetboard`. The exercises walk you through configuring content exclusions (`.copilotignore`), writing a `FLEETBOARD-COPILOT-POLICY.md`, and verifying that Copilot ghost text no longer surfaces the sensitive content.

## Files

- `src/auth.js` — FleetBoard operator auth module (the file Copilot looks at while demonstrating ghost-text completion)
- `src/boilerplate.js` — FleetBoard boilerplate the exercise opens as a second completion target
- `fleet-secrets/dispatch.yaml` — example FleetBoard dispatch config with embedded secrets (used by the exclusion exercise)
- `fleet-secrets/telemetry.pem` — example PEM blob (used by the exclusion exercise)
- `credentials.json` — example root-level credentials file (used by the exclusion exercise)
- `.env.fleetboard` — example FleetBoard environment file (used by the exclusion exercise)
- `README.md` — this file, opened in Task 9 to confirm Markdown exclusion behaviour

## Do not ship

Everything in `fleet-secrets/`, `credentials.json`, and `.env.fleetboard` is example data staged for the Copilot content-exclusion walkthrough. These files are NOT real credentials and must not be reused in any production context.
