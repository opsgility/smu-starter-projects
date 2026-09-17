# az-dev-200-module-registry

Anchorline Outdoors shared Bicep modules. Publish them to a private ACR-backed registry with semver versions, then consume from a top-level template.

## Layout

```
modules/
  storage/main.bicep      # v1.2.0
  keyvault/main.bicep     # v1.0.0
  appinsights/main.bicep  # v1.0.0
main/
  main.bicep              # top-level consumer
publish-modules.sh        # bulk publish helper
bicepconfig.json          # ACR module alias
```

## Publish

```bash
export ACR_LOGIN_SERVER=<yourregistry>.azurecr.io
./publish-modules.sh
```

## Consume from br:

Update `main/main.bicep` to import via `br:` once the alias in `bicepconfig.json` points to your registry:

```bicep
module storage 'br/anchorlineModules:storage:1.2.0' = { ... }
```

Bump the version tag on republish; consumers stay pinned until they change the version string.
