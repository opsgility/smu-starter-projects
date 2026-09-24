# SMU-ARM-FUND — ARM Templates: Fundamentals & Migration to Bicep

Starter project files for course 603 (SMU-ARM-FUND). Each hands-on lab in the course
uses a sub-subfolder here.

| Lab | Sub-subfolder | Purpose |
|---|---|---|
| Lab 02 | `lab02-first-arm/` | Storage-account ARM template to parameterize and lint |
| Lab 04 | `lab04-copy-loops/` | Scaffold VM template — students add copy, condition, dependencies |
| Lab 06 | `lab06-linked-templates/` | Monolithic template to split into main + modules + template spec + deploymentScript |
| Lab 08 | `lab08-ci-decompile/` | Pester + workflow scaffold + 3 real-world templates for `bicep decompile` |

## Ridgeway Utilities

The course anchors every lab in the fictional Ridgeway Utilities — a mid-size
municipal utility that inherited ~180 ARM JSON templates from a previous IT
contractor. The templates deploy metering, billing, and admin-portal workloads.

## Container

All labs target the `vscode-dotnet` container variant:
- Azure CLI (latest), Az PowerShell, Bicep CLI
- arm-ttk pre-installed as a system-wide PowerShell module at
  `/opt/microsoft/powershell/7/Modules/arm-ttk` — `Import-Module arm-ttk` works
- Pester, PSScriptAnalyzer, gh CLI, kubectl, helm, terraform

## Pre-created RG

Each hands-on lab attaches an ARM template that creates the pre-provisioned
resource group. Students have RG-scope Contributor and nothing else.
