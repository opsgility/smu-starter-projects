// SMU-BICEP-FUND Lab 08 — starter main.bicep
//
// State at Exercise 1 baseline: parameter shape + `existing` symbolic references
// to the pre-provisioned Key Vault and spoke VNet only. NO real resources are
// deployed yet — every downstream resource (VM, NIC, Storage, PE, DNS) is added
// by you as you author modules in Exercises 2-4.
//
//   Ex 1 — verify the pre-provisioned KV + spoke VNet exist and confirm you can
//          read the `admin-password` secret metadata as `labuser`.
//   Ex 2 — add modules/vm.bicep. Reference `kv` with `existing`, pull
//          `admin-password` via `kv.getSecret('admin-password')`, feed it into a
//          @secure() adminPassword parameter on the module, deploy a Standard_B1s
//          Ubuntu VM into `workload-subnet`.
//   Ex 3 — add modules/storage-pe.bicep. Deploy a Standard_LRS Storage account
//          with `publicNetworkAccess: 'Disabled'` + a private endpoint on
//          `workload-subnet` targeting the `blob` subresource.
//   Ex 4 — add modules/dns.bicep. Deploy `privatelink.blob.core.windows.net`,
//          link it to the spoke VNet, and attach a `privateDnsZoneGroups` child
//          on the PE so the NIC IP auto-registers as an A record.

targetScope = 'resourceGroup'

// -----------------------------------------------------------------------------
// Parameters
// -----------------------------------------------------------------------------

@description('Azure region for resources you deploy. Defaults to the RG location.')
param location string = resourceGroup().location

@description('Tag applied to all resources for cost + ownership tracking.')
param workload string = 'cascade-lab08'

@description('Name of the pre-provisioned Key Vault in this RG (the ARM template that runs at lab start creates it as kv-bicep-lab08-<uniqueString>).')
param keyVaultName string

@description('Name of the pre-provisioned spoke VNet in this RG (the ARM template creates it as `spoke-vnet`).')
param spokeVnetName string = 'spoke-vnet'

@description('Subnet in `spoke-vnet` for the VM NIC + private endpoint. Both terminate here.')
param workloadSubnetName string = 'workload-subnet'

@description('VM admin username. Never hard-code in Production — pass via CLI.')
param adminUsername string = 'cascadeadmin'

// -----------------------------------------------------------------------------
// Existing (compile-time symbolic references — the deployer never creates these)
// -----------------------------------------------------------------------------
//
// `existing` tells Bicep "look up this resource at deployment time, but do NOT
// deploy it". Both the KV and the VNet were pre-provisioned by the ARM template
// that runs at lab start. If either is missing when you deploy, ARM returns
// NotFound and the whole deployment fails.
//
// You'll use `kv.getSecret('admin-password')` in Exercise 2's module invocation
// to retrieve the admin password without ever putting it in a template file or
// deployment log — the compiler only accepts this call inside a module `params`
// block on a `@secure()` parameter.

resource kv 'Microsoft.KeyVault/vaults@2023-07-01' existing = {
  name: keyVaultName
}

resource spokeVnet 'Microsoft.Network/virtualNetworks@2023-11-01' existing = {
  name: spokeVnetName

  resource workloadSubnet 'subnets' existing = {
    name: workloadSubnetName
  }
}

// -----------------------------------------------------------------------------
// Exercise 2 will add a module reference like:
//
//   module vm 'modules/vm.bicep' = {
//     name: 'deployVm'
//     params: {
//       location: location
//       workload: workload
//       subnetId: spokeVnet::workloadSubnet.id
//       adminUsername: adminUsername
//       adminPassword: kv.getSecret('admin-password')   // <-- @secure() at module boundary
//     }
//   }
//
// Do NOT add it now — Exercise 2 walks you through authoring vm.bicep and the
// module invocation together.
// -----------------------------------------------------------------------------

// -----------------------------------------------------------------------------
// Exercise 3 will add a module reference like:
//
//   module storage 'modules/storage-pe.bicep' = {
//     name: 'deployStoragePe'
//     params: {
//       location: location
//       workload: workload
//       subnetId: spokeVnet::workloadSubnet.id
//     }
//     dependsOn: [vm]
//   }
// -----------------------------------------------------------------------------

// -----------------------------------------------------------------------------
// Exercise 4 will add a module reference like:
//
//   module dns 'modules/dns.bicep' = {
//     name: 'deployPrivateDns'
//     params: {
//       vnetId: spokeVnet.id
//       privateEndpointName: storage.outputs.privateEndpointName
//     }
//   }
// -----------------------------------------------------------------------------
