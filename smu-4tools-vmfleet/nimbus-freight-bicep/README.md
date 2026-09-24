# nimbus-freight-bicep — Lesson 6 starter (Bicep half)

Bicep scaffold for the Bicep half of Lesson 6 of course 604 (SMU-4TOOLS-VMFLEET).

## Layout

- `main.bicep` — root module composing network + compute + data.
- `network.bicep` — VNet + 4 subnets + NSG on app-subnet.
- `compute.bicep` — VMSS + 3 zonal App VMs via `[for z in range(1, 3): ...]`.
- `data.bicep` — SQL VM (base + SQL registration) + Recovery Services vault + backup policy + protected item.
- `main.parameters.json` — parameter values (adminPassword + sqlAdminPassword). **In .gitignore — never commit secrets.**
- `main.parameters.example.json` — example values with fake passwords.

## Workflow

```bash
# Compile + inspect ARM
az bicep build --file main.bicep

# What-if BEFORE deploy
az deployment group what-if -g nimbus-freight-rg --template-file main.bicep --parameters main.parameters.json

# Deploy
az deployment group create -g nimbus-freight-rg --template-file main.bicep --parameters main.parameters.json --name nimbus-fleet-bicep-$(date +%s)
```

## Files the student writes

Students author `main.bicep`, `network.bicep`, `compute.bicep`, `data.bicep` from scratch across exercises 1-4. Exercise 5 compares to the ARM version in `../nimbus-freight-arm/`.

## Files provided as scaffold

- `main.parameters.example.json` — parameter file template.
- `.gitignore` — excludes real secrets file, decompiled artifacts, and reflection notes.
