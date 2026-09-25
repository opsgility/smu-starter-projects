# SMU-ARM-FUND Lab 04 — Copy loops, conditions, and dependencies

Scaffold for Lab 04 of the ARM Templates: Fundamentals & Migration to Bicep course.

## Scenario

Ridgeway needs a template that deploys a fleet of Linux VMs for their
meter-data-processing workload. The scaffold `vmfleet.json` here deploys ONE VM
in ONE subnet with ONE NIC. You will add resource copy so the template deploys
`parameters('vmCount')` VMs, property copy so the VNet has multiple subnets, a
condition on a public IP so only VM #0 gets one, and outputs so downstream
pipeline steps can pick up the fleet's subnet IDs and VM names.

## Files

```
lab04-copy-loops/
  README.md          # this file
  vmfleet.json       # scaffold — you edit this
```

## How to run

1. Open a terminal in VS Code and sign in:
   ```bash
   az login --use-device-code
   ```
2. Follow the exercises in order. Each adds one piece — resource copy,
   property copy, condition, references, arm-ttk cleanup.
3. Use `vmCount=2` and `vmSize=Standard_B1s` throughout to keep cost down.
   End the lab as soon as you finish the last exercise.

## Authentication

Runs as `labuser` with RG-scope Contributor. Do not attempt to grant
subscription-scope roles — the lab policies will block it.

## Notes

- The scaffold `vmfleet.json` is intentionally missing copy blocks and the
  condition on the public IP. Exercises 1-4 add these.
- The scaffold IS structurally sound — `az deployment group validate` should
  pass on it as-is (with the required admin password parameter).
- arm-ttk WILL fire on the scaffold (older Compute apiVersion, no location
  parameter). Exercise 5 walks the cleanup.
