# SMU-ARM-FUND Lab 02 — Read + deploy a real ARM template

Scaffold for Lab 02 of the ARM Templates: Fundamentals & Migration to Bicep course.

## Scenario

Ridgeway Utilities inherited a bare-bones ARM template that deploys one storage
account. It works, but the name, SKU, and tags are hardcoded. You will
parameterize the template, add a variables block for tags, expose the primary
blob endpoint via an output, and prove the result clean with arm-ttk.

## Files

```
lab02-first-arm/
  README.md          # this file
  storage.json       # starting-point ARM template — you will edit this
```

## How to run

1. Open a terminal in VS Code.
2. Sign in to Azure (device code from the container):
   ```bash
   az login --use-device-code
   ```
3. Follow the exercises in order. Each exercise walks you through one edit to
   `storage.json` and one `az deployment group create` invocation to verify it.

## Authentication

Runs as the pre-configured `labuser` credential with RG-scope Contributor on the
lab's pre-created resource group. No API keys.

## Notes

- The starting `storage.json` intentionally has NO parameters, variables, or
  outputs sections. You add each in Exercises 2, 4, and 5.
- arm-ttk is pre-installed. Run `pwsh` then `Import-Module arm-ttk` then
  `Test-AzTemplate -TemplatePath ./` from this folder.
