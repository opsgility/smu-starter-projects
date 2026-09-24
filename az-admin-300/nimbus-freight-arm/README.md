# nimbus-freight-arm — Lesson 6 starter (ARM half)

Hand-written ARM JSON equivalent of the Bicep fleet in `../nimbus-freight-bicep/`.

## Purpose

Students in Exercise 5 of Lesson 6 read this file, count lines against their
Bicep implementation, and (optionally, quota permitting) deploy it to compare
head-to-head. The point is to FEEL the JSON verbosity + `dependsOn` ceremony
that Bicep abstracts away.

## Files

- `main-arm.json` — partial hand-written ARM scaffold covering the VNet + NSG (~80 lines). Students may either use `az bicep build` to produce the full compiled ARM from their Bicep authoring OR read this partial scaffold to feel the JSON verbosity.
- `main-arm.parameters.example.json` — parameter values with placeholder secrets.

## Deploy (optional)

```bash
az deployment group create \
  -g nimbus-freight-rg \
  --template-file main-arm.json \
  --parameters main-arm.parameters.json \
  --name nimbus-fleet-arm-$(date +%s)
```

## Reverse-engineer path (for the "we have an ARM template, how do we get Bicep" workflow)

```bash
az bicep decompile --file main-arm.json
# Produces main-arm.bicep — compare to nimbus-freight-bicep/main.bicep
```
