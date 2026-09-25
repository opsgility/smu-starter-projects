# SMU-4TOOLS-VMFLEET — VM Fleet Management: Four Tools, One Scenario

Starter project files for course 604 (SMU-4TOOLS-VMFLEET). The capstone of the
Azure Administrator IaC wave — deploy the same Nimbus Freight 3-tier IaaS
fleet four ways (Azure CLI, Azure PowerShell, Bicep, ARM), then survive an
AI-graded incident-response drill.

| Lab | Sub-subfolder | Purpose |
|---|---|---|
| Lab 02 | `nimbus-freight-cli/` | Bash script scaffolds — `deploy-nimbus-freight.sh` assembled across 7 exercises |
| Lab 04 | `nimbus-freight-ps/` | Azure PowerShell scaffolds — `Deploy-NimbusFreight.ps1` |
| Lab 06 | `nimbus-freight-bicep/` | Bicep modules — `main.bicep` + `network.bicep` + `compute.bicep` + `data.bicep` |
| Lab 06 | `nimbus-freight-arm/` | Hand-written ARM JSON equivalent of the Bicep fleet |
| Lab 07 | `nimbus-freight-incident/` | Broken-fleet scenario data for the capstone challenge |

## Nimbus Freight

The course anchors every lab in the fictional **Nimbus Freight** — a mid-size
regional logistics carrier running an internal order-tracking IaaS web app:

- **Web tier** — VMSS (Standard_B2s x 3, zone-redundant) behind Application Gateway v2 with WAF.
- **App tier** — 3 zonal VMs (Standard_B2s), one per Availability Zone in eastus2.
- **Data tier** — 1 SQL VM (Standard_D2s_v3 or Standard_DS2_v2 fallback).
- **Backup** — Recovery Services vault + backup policy protecting the SQL VM.

The exact same fleet is deployed four different ways in labs 2, 4, and 6 — so
the value is in the head-to-head comparison of tool ergonomics, not in
re-teaching each tool from scratch.

## Container

All labs target the `vscode-dotnet` container variant. Pre-installed tooling:

- Azure CLI (latest, unpinned)
- Azure PowerShell 7 + Az module + PSRule.Rules.Azure + Pester + PSScriptAnalyzer
- Bicep CLI + `ms-azuretools.vscode-bicep` VS Code extension
- `arm-ttk` cloned into `/opt/microsoft/powershell/7/Modules/arm-ttk` (`Import-Module arm-ttk` works)
- azd, kubelogin, yq, terraform + tflint, kustomize
- .NET 9 + .NET 10 SDKs, gh CLI, kubectl, helm, Docker CLI

## Pre-created RG

Every hands-on lab attaches an ARM template that pre-provisions the
`nimbus-freight-rg` resource group. Students have RG-scope Contributor and
nothing else (no Owner, no subscription-scope permissions).

## Subscription pool

Pool 5 (standard IaaS) for all hands-on labs and the capstone challenge.
