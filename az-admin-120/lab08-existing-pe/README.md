# SMU-BICEP-FUND Lab 08 — Reference an existing Key Vault + Storage private endpoint + private DNS

Starter scaffold for Lab 08 of the *Bicep Fundamentals for Azure Infrastructure* course.

## Scenario

Cascade Renewable Energy's platform team has centralised secret management in
Key Vault and standardised on Private Link for every PaaS surface. Your job is
to author Bicep that consumes an *existing* Key Vault (created by the platform
team, not by you), then land a Storage account behind a Private Endpoint on the
spoke VNet — with Blob public access disabled and a `privatelink.blob.core.windows.net`
private DNS zone linked to the spoke so the storage FQDN resolves to the PE's
NIC IP.

The Key Vault, its `admin-password` secret, and the spoke VNet are all
pre-provisioned in the lab RG by an ARM template that runs at lab start (allow
~10 minutes). You reference them with the Bicep `existing` keyword and
`kv.getSecret('admin-password')` — you never create them, and the secret value
never leaves the Bicep compiler's memory.

## Files

```
lab08-existing-pe/
  README.md               # this file
  main.bicep              # starter — declares the workload parameters and pre-created resource references
  modules/                # you create these in Exercises 2-4
    vm.bicep              # you author this in Exercise 2 (VM with secure adminPassword)
    storage-pe.bicep      # you author this in Exercise 3 (Storage account + PE)
    dns.bicep             # you author this in Exercise 4 (private DNS zone + vnet link + zone group)
  bicepconfig.json        # minimal linter config
```

`main.bicep` starts with only the parameter shape and `existing` symbolic
references to the pre-provisioned KV and VNet. Every real resource (VM, NIC,
Storage, PE, DNS zone, vnet link, zone group) is added by you as you author
the modules in Exercises 2-4.

## How to run

1. Sign into Azure in the VS Code terminal:
   ```bash
   az login --use-device-code
   ```
   Follow the device-code flow in a private/incognito browser using the lab
   credentials shown on the Environment tab.

2. Confirm the pre-created resources are present (the ARM template that runs
   at lab start provisions these — allow ~10 minutes if the lab just started):
   ```bash
   RG=$(az group list --query "[?starts_with(name, 'cascade-')].name | [0]" -o tsv)
   KV=$(az keyvault list -g "$RG" --query "[0].name" -o tsv)
   VNET=$(az network vnet list -g "$RG" --query "[?name=='spoke-vnet'].name | [0]" -o tsv)
   echo "RG=$RG  KV=$KV  VNET=$VNET"
   ```
   All three variables must be non-empty before you start Exercise 2. If any
   are empty, wait 60 seconds and retry — the ARM template is still running.

3. Follow the exercises in order. Each exercise incrementally deploys `main.bicep`.

## Authentication

Runs as `labuser` (RG-scope Owner on the pre-created `cascade-*` resource
group; subscription-scope `LabUserRole` for `az keyvault list` and
`az deployment` preview only). The lab platform has also granted `labuser`
`Key Vault Secrets User` on the pre-provisioned Key Vault so
`kv.getSecret('admin-password')` succeeds from your Bicep deployment context.

You do NOT need to grant yourself any additional RBAC. If `az deployment group
create` returns `Forbidden` on the KV `getSecret` call, wait 60 seconds for
RBAC propagation and retry — do not add roles to your credential.

## Notes

- Bicep CLI is preinstalled in the `vscode-dotnet` container. `bicep --version`
  works out of the box; no `az bicep install` step required.
- The `existing` keyword is compile-time — it declares a symbolic reference the
  Bicep transpiler resolves against the runtime resource. If the resource is
  not present at deployment time, ARM returns `NotFound` and the whole
  deployment fails.
- `kv.getSecret('admin-password')` can ONLY appear inside a module `params`
  block on a parameter decorated `@secure()`. The compiler enforces this — the
  secret literal never lands in a template or deployment log.
- Private endpoints require `privateEndpointNetworkPolicies=Disabled` on the
  subnet. `workload-subnet` is pre-provisioned with that flag set.
- The private DNS zone name for Blob storage is exactly
  `privatelink.blob.core.windows.net` (from the MS Learn "Azure Private Endpoint
  private DNS zone values" reference). Any other name and the auto-registration
  A-record won't resolve the storage FQDN to the PE IP.
- The `privateDnsZoneGroups` child resource on the PE automatically registers
  the A-record for the PE NIC IP into the linked zone — you do NOT create the
  A-record yourself.
