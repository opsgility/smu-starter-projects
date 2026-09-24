# SMU-ARM-FUND Lab 08 — Test in CI + decompile a real ARM template to Bicep

Scaffold for Lab 08 of the ARM Templates: Fundamentals & Migration to Bicep course.

## Scenario

Ridgeway's Bicep migration is real, but the team is starting with three legacy
ARM templates the platform runs today: a VMSS + Load Balancer + VNet + NSG
composition, an App Service + SQL DB pair, and an AKS + ACR + Key Vault
composition. You will (1) build a GitHub Actions gate that runs arm-ttk via
Pester, `az deployment group validate`, and `az deployment group what-if` on
every PR — blocking merges that add lint issues or predict unintended
deletions — and (2) decompile one of the templates to Bicep with `bicep
decompile`, catalog the artifacts, clean them up, and write a keep-vs-migrate
verdict per template.

## Files

```
lab08-ci-decompile/
  README.md                                     # this file
  tests/
    README.md                                   # you add ArmTtk.Tests.ps1 here
  .github/
    workflows/
      README.md                                 # you add arm-tests.yml here
  legacy-arm-templates/
    vmss-lb-vnet-nsg/main.json                  # ~400-line real-world template
    app-service-sql/main.json                   # ~250-line real-world template
    aks-acr-keyvault/main.json                  # ~500-line real-world template
```

## How to run

1. Sign in:
   ```bash
   az login --use-device-code
   ```
2. Exercise 1: write `tests/ArmTtk.Tests.ps1` and run it locally.
3. Exercise 2: write `.github/workflows/arm-tests.yml`.
4. Exercise 3: `bicep decompile legacy-arm-templates/vmss-lb-vnet-nsg/main.json`.
5. Exercise 4: catalog decompilation artifacts.
6. Exercise 5: extract modules, clean up, verify with `bicep build` and `az deployment group what-if`.
7. Exercise 6: write `verdicts.md` — keep / migrate / leave per template.

## Authentication

Runs as `labuser` (RG-scope Contributor). The workflow shown in Exercise 2 uses
Azure OIDC federated login — see `learn.microsoft.com/azure/developer/github/connect-from-azure`
for setup. You will not actually run the workflow against Azure in this lab —
authoring the YAML is the exercise.

## Notes

- The three `legacy-arm-templates/` intentionally have arm-ttk findings — some
  older apiVersions, some redundant `dependsOn` — because that's the teaching
  point of Exercise 4 (catalog decompilation artifacts).
- The `tests/README.md` and `.github/workflows/README.md` scaffolds are
  intentionally empty prompts. You add the real files during the exercises.
- Cost: only Exercise 5's optional actual deploy costs anything (VMSS instances).
  Skip it if you want to keep the run free.
