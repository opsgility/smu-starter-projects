# Engineering at Northwind Logistics

Welcome to the Northwind engineering wiki. This page is the entry point for new engineers. We ship internal services that move freight from origin to destination — our codebase is largely TypeScript and Python, deployed to Azure.

## Core principles

- **Operational empathy** — every service we ship has a runbook before it has a launch announcement.
- **Tracing first** — OpenTelemetry is enabled by default; no service ships without spans.
- **Tenancy enforced at the edge** — every authenticated request carries a tenant id; no internal call is trusted blindly.

## Where to look next

- `wiki://onboarding` — your first two weeks
- `wiki://incident-response` — how we respond to outages
- `playbook://outage` — the on-call outage runbook
