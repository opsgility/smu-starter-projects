# nimbus-freight-cli — Lesson 2 starter

Bash + Azure CLI scaffold for Lesson 2 of course 604 (SMU-4TOOLS-VMFLEET).

Across the 7 exercises the student:
1. Writes `1-network.sh` through `6-backup.sh` (one per resource group of exercises).
2. Consolidates them into a single `deploy-nimbus-freight.sh` at the end.
3. Writes `REFLECTION.md` capturing ergonomic pain points to compare against L4 (PS) and L6 (Bicep + ARM).

## Files provided

- `web-cloud-init.yaml` — cloud-init file for VMSS instances (nginx + Nimbus Freight index).
- `deploy-nimbus-freight.sh.template` — skeleton the student pastes command blocks into.
- `.gitignore` — excludes local secrets and the consolidated script's outputs.
