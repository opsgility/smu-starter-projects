# nimbus-freight-incident — Lesson 7 starter (capstone challenge)

Broken-fleet scenario data for the AI-graded VM Challenge in Lesson 7 of course 604 (SMU-4TOOLS-VMFLEET).

## Purpose

The capstone lab pre-provisions the full Nimbus Freight fleet in a state of degraded production, then hands the student the incident. The student must diagnose, remediate, codify, and defend.

## The three failures

The lab's ARM template introduces three deliberate misconfigurations (do NOT show these to students — they must diagnose):

1. **App Gateway backend health probe path is misconfigured.** Set to `/` on nginx configured to serve health on `/healthz` — probes return 404, backend pool marked unhealthy.
2. **Azure Backup protection state is `ProtectionStopped`.** Protection was enabled at deploy, then explicitly stopped via `az backup protection disable --retain-recovery-points`. No scheduled backups run.
3. **The three App VMs' NIC-attached NSG blocks port 22 AND port 8080.** Result: `az vm run-command invoke` still works (uses Azure agent channel), but the app VMs are unreachable via SSH AND on the app port. Student diagnoses via `az vm run-command invoke` for the "echo ok" test.

## Files provided

- `INCIDENT-BRIEF.md` — the fictional SLO team's page that the student receives at lab start.
- `DECISION-LOG.template.md` — 300-word template the student fills out and commits.

## Grading

See `RecordChallengeToolInstructions` on lab 2971. Four criteria (Diagnose, Remediate, Codify, Defend) — all four must pass.
