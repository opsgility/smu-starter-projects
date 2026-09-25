# nimbus-freight-ps — Lesson 4 starter

Azure PowerShell scaffold for Lesson 4 of course 604 (SMU-4TOOLS-VMFLEET).

Across 7 exercises the student:
1. Writes `1-Network.ps1` through `6-Backup.ps1` — one per resource area.
2. Consolidates into `Deploy-NimbusFreight.ps1` with a proper `param()` block.
3. Writes `REFLECTION-PS.md` comparing LOC + splatting subjective read + would-you-ship-as-source-of-truth against L2's bash implementation.

## Files provided

- `Deploy-NimbusFreight.ps1.template` — skeleton with param() + strict mode + placeholders.
- `.gitignore` — excludes local secrets and reflection notes.

## Pattern hints

- Pipeline objects: `$vnet = New-AzVirtualNetwork ...`, then `$vnet.Subnets[0].Id` downstream.
- Splatting for App Gateway: build `$agwParams = @{ ... }`, call `New-AzApplicationGateway @agwParams`.
- Ambient context: `Set-AzRecoveryServicesVaultContext -Vault $vault` — subsequent backup cmdlets need no `-VaultName`.
- `foreach ($z in 1..3) { ... }` for the three App VMs.
