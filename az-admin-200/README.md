# az-admin-200 — AZ-ADMIN-200: Enterprise Landing Zone with Bicep and azd

Starter projects for course **AZ-ADMIN-200** (SkillMeUp course id 600).

Each sub-subfolder is the starter for one hands-on lab. The student's VS Code container clones this repo at startup and opens the relevant `lab-*/` directory as its workspace.

## Labs

| Sub-subfolder | Lab | Status |
|---|---|---|
| `lab-02-azd-bootstrap/` | Bootstrap an azd project with a hub VNet + Log Analytics baseline | scaffold — authoring pending |
| `lab-04-avm-and-acr/`   | Compose the LZ with AVM modules + a private ACR registry | scaffold — authoring pending |
| `lab-06-dns-rbac-kv/`   | Wire private DNS + RBAC baseline + shared Key Vault | scaffold — authoring pending |
| `lab-08-policy-psrule/` | Deploy CAF-aligned Azure Policy assignments + gate the LZ on PSRule | scaffold — authoring pending |

## References

Cross-lab references live under `references/`:
- `references/naming-convention.md` — CAF-aligned resource naming scheme used across the LZ.
- `references/policy-catalog.md` — canonical policy set the labs assign in lab-08.

## Conventions

- Sub-subfolder naming uses `lab-NN-<slug>` (hyphenated form) matching the platform's `StarterProjectSubfolder` wiring for this course.
- `azd-lz/` under lab-02 holds the shared azd project skeleton subsequent labs build on.
- No secrets committed. Subscription/tenant scoping happens at azd env init time.
