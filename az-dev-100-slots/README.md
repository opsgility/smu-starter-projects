# AZ-DEV-100 · Module 4 Lab — Deployment slots and blue/green

Extends Module 3's OIDC pipeline with a staging slot so you can rehearse deploys before they hit production. The starter's `/version` endpoint reports the slot name (from `WEBSITE_SLOT_NAME`) — swap-visible proof that the swap actually moved which slot serves prod.

## Scenario

Anchorline's storefront now ships via GitHub Actions on push to main (Module 3). This module adds the staging slot + swap safety net you'll use on every production Web App from here forward.

## Files

```
az-dev-100-slots/
  README.md
  .gitignore
  Project.csproj                # net10.0
  Program.cs                    # /health, /version (includes slotName)
  appsettings.json
  appsettings.Development.json
  Properties/launchSettings.json
```

## The `/version` endpoint

Returns:
```json
{
  "buildTag": "v4.0.0-anchorline-slots-baseline",
  "slotName": "production",
  "dotnetVersion": "10.0.0",
  "environment": "Production"
}
```

The `slotName` field reads from the `WEBSITE_SLOT_NAME` env var App Service injects into every slot's process — `production` on the default slot, `staging` on the staging slot. After a swap, curling the production hostname returns `slotName: "production"` (the swap put the staging bits on the production label).

## Deploy

The lab's ARM template pre-provisions:
- A Standard S1 Linux App Service Plan.
- A Web App with the default (production) slot.
- A **staging slot** already created (a distinct `-staging.azurewebsites.net` hostname).
- A user-assigned MI with `Website Contributor` on the Web App (inherited by both slots).

Deploy to staging:

```bash
az webapp deploy --resource-group $RG --name $WEBAPP --slot staging --src-path ./app.zip --type zip
```

Warm up staging, smoke test, then swap:

```bash
az webapp deployment slot swap --resource-group $RG --name $WEBAPP --slot staging --target-slot production
```

## Notes

- **`WEBSITE_SLOT_NAME` is a platform-managed env var**, not something you set in an app setting. It's always `production` on the default slot, `<slot-name>` on staging slots.
- **Staging slot's own hostname** is `<webAppName>-staging.azurewebsites.net`. That's what you curl for smoke tests.
- **`applicationInitialization`** — for Linux there's no `web.config`, so use the `WEBSITE_SWAP_WARMUP_PING_PATH` app setting instead (set on the staging slot).
- **This module does NOT change the OIDC federated credential** — the UAMI from Module 3 already has Website Contributor on the Web App resource, which inherits down to slot subresources.
