# az-dev-200-psrule-pester

Anchorline Bicep tested with three gates: `bicep lint`, PSRule for Azure (`Azure.Default` baseline), and Pester unit tests.

## Run locally

```bash
az bicep lint --file main.bicep
```

```powershell
Install-Module PSRule.Rules.Azure -Force
Assert-PSRule -InputPath 'main.bicep' -Module PSRule.Rules.Azure -Baseline Azure.Default

Install-Module Pester -Force
Invoke-Pester ./tests
```

## Introduce a violation and watch CI block

Set `allowBlobPublicAccess: true` on the Storage Account, push a PR. PSRule fires `Azure.Storage.BlobPublicAccess`; the workflow fails; the PR cannot merge.
