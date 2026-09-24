# SMU-ARM-FUND Lab 06 — Linked templates + template spec + deploymentScript

Scaffold for Lab 06 of the ARM Templates: Fundamentals & Migration to Bicep course.

## Scenario

Ridgeway inherited a ~300-line monolithic ARM template that deploys a VNet plus
a Storage Account together. It works, but every change requires a diff review
of the whole file and every workload team has copied the same shape. You will
split it into modules, wire them via linked templates, publish the VNet as a
versioned template spec, and add a deploymentScript that seeds a blob container
after the storage account provisions.

## Files

```
lab06-linked-templates/
  README.md              # this file
  original.json          # the monolithic ARM template you split apart
  main.json              # scaffold orchestrator you fill in
  modules/
    vnet.json            # scaffold module — extract from original.json
    storage.json         # scaffold module — extract from original.json
```

## How to run

1. Open a terminal and sign in:
   ```bash
   az login --use-device-code
   ```
2. Follow the exercises in order:
   1. Split `original.json` into `main.json` + `modules/vnet.json` + `modules/storage.json`
   2. Wire the modules via linked templates (blob storage + SAS)
   3. Publish `vnet.json` as a template spec via `az ts create`
   4. Add a deploymentScript that runs `az storage container create`
   5. Deploy the full composition and verify

## Authentication

Runs as `labuser` (RG-scope Contributor). The deploymentScript exercise creates
a user-assigned Managed Identity and grants it Storage Blob Data Contributor on
the storage account created by the module. All within RG scope — no sub-scope
role grants required.

## Notes

- The `main.json` scaffold ships mostly empty on purpose. Exercise 2 has you
  fill in the two linked-template `deployments` resources.
- The `modules/` files start as copies of `original.json` — you trim each
  down to just the resource type + parameters + outputs for that module.
- deploymentScripts require an ACI to spin up and tear down; expect ~5-8 min
  extra deployment time in Exercise 4.
