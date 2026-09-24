// SMU-BICEP-FUND Lab 04 — starter main.bicep
//
// State at Exercise 1: one inline VNet with two subnets, hard-wired names,
// deployed at RG scope. You will refactor this in place across Exercises 2-5:
//   Ex 2 — extract the VNet resource into modules/vnet.bicep
//   Ex 3 — call the module twice (hub-vnet + spoke-vnet) with different params
//   Ex 4 — add a bidirectional peering (inline or via modules/peering.bicep)
//   Ex 5 — surface the subnet resource IDs at main.bicep level via outputs

targetScope = 'resourceGroup'

@description('Azure region for all resources. Defaults to the RG location.')
param location string = resourceGroup().location

@description('Tag applied to all resources for cost + ownership tracking.')
param workload string = 'cascade-lab04'

// -----------------------------------------------------------------------------
// Exercise 1 baseline: single inline VNet, two /24 subnets, no peering.
// -----------------------------------------------------------------------------

resource vnet 'Microsoft.Network/virtualNetworks@2023-11-01' = {
  name: '${workload}-vnet'
  location: location
  tags: {
    workload: workload
    lesson: 'lab04-modules-vnet'
  }
  properties: {
    addressSpace: {
      addressPrefixes: [
        '10.0.0.0/16'
      ]
    }
    subnets: [
      {
        name: 'app'
        properties: {
          addressPrefix: '10.0.1.0/24'
        }
      }
      {
        name: 'data'
        properties: {
          addressPrefix: '10.0.2.0/24'
        }
      }
    ]
  }
}

output vnetName string = vnet.name
output vnetId string = vnet.id
