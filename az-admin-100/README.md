# az-admin-100 — AZ-ADMIN-100: Azure CLI Essentials for IaaS Administrators

Starter projects for course **AZ-ADMIN-100** (SkillMeUp course id 602).

Each sub-subfolder is the starter for one hands-on lab. The student's VS Code container clones this repo at startup and opens the relevant `lab*/` directory as its workspace.

## Labs

| Sub-subfolder | Lab | Status |
|---|---|---|
| `lab02-defaults-query/` | Your first admin CLI workflow — set defaults, query resources, extract IDs for pipelines | authoring pending |
| `lab04-vm-disks/` | Deploy VMs, snapshot the OS disk, restore into a clone | authoring pending |
| `lab06-networking/` | Build a hub-spoke topology with NSGs, service tags, and peering | authored (sourceable helpers) |
| `lab08-storage-mi/` | Storage with private access plus AzCopy plus managed-identity authenticated access | authored (sourceable helpers) |
| `lab10-robust-scripts/` | Ship a robust admin script — bash toolkit, GitHub Actions workflow, and OIDC-authenticated cross-sub run | authoring pending |

## Conventions

- One folder per hands-on lab, named `labNN-<slug>`.
- `helpers.sh` is a sourceable bash file — the exercise text guides the student to `source helpers.sh` and call named functions rather than copy-pasting long `az ...` incantations.
- No secrets committed. Region defaults live in the exercise text, not in the starter.
