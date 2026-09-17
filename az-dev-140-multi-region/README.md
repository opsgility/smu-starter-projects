# az-dev-140-multi-region

Demonstrate multi-region write conflicts and last-writer-wins resolution.

## Env

- `ANCHORLINE_COSMOS_ENDPOINT` — account with multi-region writes ENABLED
- `ANCHORLINE_REGION_1` — first write region (default "East US 2")
- `ANCHORLINE_REGION_2` — second write region (default "West US 2")

## Modes

```
dotnet run --project . -- seed          # seed prod-4s-tent = $599 in region 1
dotnet run --project . -- conflict-lww  # simultaneous writes $650 (r1) and $625 (r2); watch LWW resolve
dotnet run --project . -- show          # read from each region
```
