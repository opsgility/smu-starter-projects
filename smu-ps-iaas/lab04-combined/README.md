# SMU-PS-IAAS Lesson 4 — Combined Hub-Spoke, Storage, RBAC, Batch Ops

Starter project for **Lesson 4** of *Azure PowerShell for IaaS Administrators*.
This is the capstone lesson: you build a small module (`AzureAdminHelpers.psm1`)
plus a suite of scripts that stand up a hub-spoke network, create a storage
account with a lifecycle policy, assign RBAC to a lab identity, and generate a
one-page HTML inventory (`inventory.html`) of everything the module produced.

## Scenario

You've been asked by **Contoso Distribution** to package the ad-hoc scripts you
wrote across lessons 1-3 into a reusable module the whole IaaS team can dot-source.
Everything you build here must be idempotent, take parameters (no hardcoded
names), and emit structured output an HTML reporter can consume.

## Files

```
smu-ps-iaas/lab04-combined/
  README.md                    # This file.
  .gitignore                   # Ignores local secrets, transcripts, PowerShell caches.
  Utils.psm1                   # Shared helpers: Get-LabResourceGroupName,
                               # Get-DefaultLocation, Assert-AzContext,
                               # New-LabResourceGroupIfMissing, Get-LabTag.
  Scripts/                     # Empty at start of lesson. You will create:
    .gitkeep                   #   - AzureAdminHelpers.psm1  (Task 1)
                               #   - Deploy-HubSpoke.ps1      (Task 2)
                               #   - New-LabStorage.ps1       (Task 3)
                               #   - Grant-LabRoles.ps1       (Task 4)
                               #   - inventory.html           (Task 5 output)
```

## How to run

1. Open a PowerShell 7 terminal in the container (`pwsh`).
2. Sign in with device code — the container is headless, browser popups won't work:

   ```powershell
   Connect-AzAccount -UseDeviceAuthentication
   ```

3. Confirm your context and the pre-created RG the lab provisioned:

   ```powershell
   Import-Module ./Utils.psm1 -Force
   Assert-AzContext
   Get-AzResourceGroup -Name (Get-LabResourceGroupName)
   ```

4. Build the scripts under `Scripts/` as the exercise walks you through. Each
   script loads the shared helpers at the top:

   ```powershell
   Import-Module (Join-Path $PSScriptRoot '..' 'Utils.psm1') -Force
   Import-Module "$PSScriptRoot/AzureAdminHelpers.psm1" -Force
   Assert-AzContext
   ```

5. Run them in order:

   ```powershell
   ./Scripts/Deploy-HubSpoke.ps1
   ./Scripts/New-LabStorage.ps1
   ./Scripts/Grant-LabRoles.ps1
   ```

## Authentication

The lab attaches a credential named `psiaaslabuser` with **Contributor** at the
pre-created resource group scope plus **User Access Administrator** at the same
scope (so Task 4's `New-AzRoleAssignment` calls succeed). All Az cmdlets pick
up the identity automatically after `Connect-AzAccount -UseDeviceAuthentication`.
No service principal keys.

## Notes

- `Utils.psm1` is kept in sync with `smu-ps-iaas/lab02-vm-disks/Utils.psm1`.
  When you touch one, touch the other in the same PR so the two lessons don't
  diverge.
- `Get-LabResourceGroupName -Suffix 'network'` gives you a separate RG name for
  the hub-spoke deployment if the exercise asks you to isolate the network
  resources — the base RG name comes from `$env:LAB_RESOURCE_GROUP`.
- `Get-LabTag` returns the standard `course` / `managed_by` / `environment`
  tag block — apply it to every resource so the cleanup script at the end of
  the lesson can find them.
- Save all your scripts under `Scripts/`. The container's file watcher picks
  them up immediately; no restart needed.
