# SMU-BICEP-FUND Lab 10 — Deployment stacks + deny-settings + CI gates

Starter scaffold for Lab 10 of the *Bicep Fundamentals for Azure Infrastructure* course.

## Scenario

Cascade Renewable Energy's platform team is done shipping hub-and-spoke VNet
templates by copy-paste. Two recent incidents forced the change:

1. An on-call engineer `az group delete`-d a shared spoke VNet in dev. There
   was no lock, no ownership record, and no way to detect the drift after the
   fact.
2. A junior dev merged a PR that added a Storage Account with
   `allowBlobPublicAccess: true`. Nothing in CI caught it; the drift was found
   two weeks later during an audit.

You are going to fix both problems in one lab:

1. Convert the deployed workload to a **deployment stack** — a single tracked
   resource that owns the VNets, subnets, and peerings and enforces
   `denyDelete` on every managed resource.
2. Add a **GitHub Actions gate** that runs `bicep build`, `bicep lint`, and
   PSRule.Rules.Azure on every PR — so bad templates never merge in the first
   place.

## Files

```
lab10-stacks-ci/
  README.md                     # this file
  main.bicep                    # starter — hub + spoke workload from lesson 4
  bicepconfig.json              # linter config (same shape as lab04/06/08)
  ps-rule.yaml                  # PSRule config (canonical Quickstart shape)
  .github/
    workflows/                  # you create gate.yml here in Exercise 4
```

`main.bicep` is a working single-file hub-and-spoke VNet workload — the same
topology you built as a set of modules in Lesson 4, flattened here so the
whole thing can be tracked by a single deployment stack from the start. You
convert this workload to a stack in Exercise 1 and keep iterating on the
SAME file across every exercise.

## How to run

1. Sign into Azure in the VS Code terminal:
   ```bash
   az login --use-device-code
   ```
   Follow the device-code flow in a private/incognito browser using the lab
   credentials shown on the Environment tab.

2. Confirm the pre-created resource group is present:
   ```bash
   RG=$(az group list --query "[?starts_with(name, 'cascade-')].name | [0]" -o tsv)
   echo "Working in: $RG"
   ```

3. Follow the exercises in the right-hand pane in order.

## Authentication

Runs as `labuser` (RG-scope Owner on the pre-created `cascade-*` resource
group) with a minimal subscription-scope role (`LabUserRole`) that permits
`az group list` and template preview only. Every resource in this lab
deploys inside the pre-created RG — no subscription-scope operations
required.

## Notes

- Bicep CLI is preinstalled in the `vscode-dotnet` container. `bicep --version`
  works out of the box — no `az bicep install` step required.
- PowerShell 7 (`pwsh`) is preinstalled, and so are the `PSRule.Rules.Azure`
  and `Pester` modules. `Invoke-PSRule` works out of the box.
- The linter runs on every save through the VS Code Bicep extension. The
  command-line equivalent (`bicep lint main.bicep`) uses the rules declared in
  `bicepconfig.json`.
- The `.github/workflows/` directory is intentionally empty — you author
  `gate.yml` there in Exercise 4.
