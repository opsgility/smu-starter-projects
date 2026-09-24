# SMU-BICEP-FUND Lab 04 — Build a modular Bicep project (Hub + Spoke VNet module)

Starter scaffold for Lab 04 of the *Bicep Fundamentals for Azure Infrastructure* course.

## Scenario

You inherited a hub-and-spoke landing-zone spec from Cascade Renewable Energy's
platform team. Every workload spins up its own VNet by copying the same 60-line
inline Bicep block. Change one address prefix and you have to hunt it across
every deployment. In this lab you extract the VNet shape into a single reusable
Bicep module, call it twice (hub + spoke), wire a bidirectional peering, and
surface subnet IDs as outputs so downstream modules (Bastion, Private Endpoints,
Firewall) can consume them.

## Files

```
lab04-modules-vnet/
  README.md                     # this file
  main.bicep                    # starter — single VNet with inline subnets (Exercise 1)
  modules/                      # you create this in Exercise 2
    vnet.bicep                  # you author this in Exercise 2
    peering.bicep               # you author this in Exercise 4
  bicepconfig.json              # minimal linter config
```

`main.bicep` starts as a single inline VNet at RG scope so Exercise 1 has a
concrete "before" state that compiles and deploys. Exercises 2 through 5
refactor it in place.

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

3. Preview and deploy the starter template as-is, then follow the exercises
   in order.

## Authentication

Runs as `labuser` (RG-scope Owner on the pre-created `cascade-*` resource
group) with a minimal subscription-scope role that permits `az group list`
and template preview only. All resources you create in this lab deploy
inside that pre-created RG — no subscription-scope operations required.

## Notes

- Bicep CLI is preinstalled in the `vscode-dotnet` container. `bicep --version`
  works out of the box; no `az bicep install` step required.
- The linter runs on every save through the VS Code Bicep extension. Warnings
  about `no-hardcoded-location` are expected until Exercise 3 parameterizes
  the location.
- VNet peering resources are child resources of `virtualNetworks`. When you
  extract them into `peering.bicep` (Exercise 4), each peering resource needs
  the parent VNet as a symbolic reference — the module receives the two VNet
  resource IDs as parameters and uses `existing` declarations to attach.
