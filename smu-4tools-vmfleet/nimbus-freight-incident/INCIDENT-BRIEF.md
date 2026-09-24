# INCIDENT-BRIEF — Nimbus Freight, page received at lab start

**From:** Nimbus Freight SLO team on-call
**Priority:** P1 — production impact
**Time:** now
**On-call engineer:** you

## Symptoms

- Customer-facing order-tracking web app is returning 502 for ~40% of requests.
- Overnight backup report shows no successful SQL backup for the past 3 nights.
- SSH bastion reports the app-tier VMs are unreachable.

## What we know

- The fleet is the standard Nimbus Freight 3-tier IaaS shape (VMSS behind App Gateway, 3 zonal App VMs, SQL VM, Recovery Services vault).
- The fleet was deployed cleanly two weeks ago via `main.bicep`.
- Someone made changes yesterday — audit trail unclear.

## Your job

1. Diagnose all three symptoms — root cause per issue.
2. Remediate each. Backend pool must return to healthy, Azure Backup must resume snapshotting the SQL VM, all three App VMs must respond.
3. Codify at least ONE fix back into the appropriate IaC repo (nimbus-freight-cli, nimbus-freight-ps, nimbus-freight-bicep, or nimbus-freight-arm).
4. Write `DECISION-LOG.md` — 300 words TOTAL — defending your tool choice at each phase against the L1 decision matrix.

The LeftAgent will coach on request but will not solve for you. Grading happens automatically against four criteria: diagnosis complete, remediation verified, codify-back commit present, decision log defensible.

## What you have

- The full VS Code container with all four course tools (az CLI, Az PS, Bicep, arm-ttk).
- RG-scope Contributor on `nimbus-freight-rg`.
- Read/write access to all four starter subfolders in `~/lab/smu-4tools-vmfleet/`.

Good luck.
