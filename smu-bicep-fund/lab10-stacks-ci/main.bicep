// SMU-BICEP-FUND Lab 10 — starter main.bicep
//
// Self-contained hub-and-spoke VNet workload. This is the SAME topology you
// built as separate modules in Lesson 4, flattened into one file so a single
// deployment stack can own the whole thing.
//
// State at Exercise 1 baseline: two VNets (hub + spoke) with a peering pair,
// deployed at RG scope as a plain deployment (no stack yet). You convert this
// to a stack in Exercise 1 and iterate on it in Exercises 2, 3, and 5.
//
//   Ex 1 — deploy as a stack with `az stack group create`
//          + `--action-on-unmanage detachAll --deny-settings-mode denyDelete`
//   Ex 2 — preview a change (new subnet) with `az stack-whatif group create`
//   Ex 3 — run PSRule.Rules.Azure locally against this file
//   Ex 4 — add a GitHub Actions gate.yml that runs bicep + PSRule on PR
//   Ex 5 — introduce a PSRule failure (public-access Storage), see it flagged

targetScope = 'resourceGroup'

// -----------------------------------------------------------------------------
// Parameters
// -----------------------------------------------------------------------------

@description('Azure region for all resources. Defaults to the RG location.')
param location string = resourceGroup().location

@description('Tag applied to every resource for cost and ownership tracking.')
param workload string = 'cascade-lab10'

// -----------------------------------------------------------------------------
// Hub VNet — 10.0.0.0/16, GatewaySubnet + AzureBastionSubnet.
// (Reserved subnet names are required by Azure at these exact spellings.)
// -----------------------------------------------------------------------------

resource hubVnet 'Microsoft.Network/virtualNetworks@2023-11-01' = {
  name: '${workload}-hub-vnet'
  location: location
  tags: {
    workload: workload
    lesson: 'lab10-stacks-ci'
    role: 'hub'
  }
  properties: {
    addressSpace: {
      addressPrefixes: [
        '10.0.0.0/16'
      ]
    }
    subnets: [
      {
        name: 'GatewaySubnet'
        properties: {
          addressPrefix: '10.0.0.0/27'
        }
      }
      {
        name: 'AzureBastionSubnet'
        properties: {
          addressPrefix: '10.0.1.0/26'
        }
      }
    ]
  }
}

// -----------------------------------------------------------------------------
// Spoke VNet — 10.1.0.0/16, workload + database subnets.
// -----------------------------------------------------------------------------

resource spokeVnet 'Microsoft.Network/virtualNetworks@2023-11-01' = {
  name: '${workload}-spoke-vnet'
  location: location
  tags: {
    workload: workload
    lesson: 'lab10-stacks-ci'
    role: 'spoke'
  }
  properties: {
    addressSpace: {
      addressPrefixes: [
        '10.1.0.0/16'
      ]
    }
    subnets: [
      {
        name: 'workload'
        properties: {
          addressPrefix: '10.1.1.0/24'
        }
      }
      {
        name: 'database'
        properties: {
          addressPrefix: '10.1.2.0/24'
        }
      }
    ]
  }
}

// -----------------------------------------------------------------------------
// Bidirectional peering (both halves required for state=Connected).
// -----------------------------------------------------------------------------

resource hubToSpoke 'Microsoft.Network/virtualNetworks/virtualNetworkPeerings@2023-11-01' = {
  parent: hubVnet
  name: 'hub-to-spoke'
  properties: {
    allowVirtualNetworkAccess: true
    allowForwardedTraffic: false
    remoteVirtualNetwork: {
      id: spokeVnet.id
    }
  }
}

resource spokeToHub 'Microsoft.Network/virtualNetworks/virtualNetworkPeerings@2023-11-01' = {
  parent: spokeVnet
  name: 'spoke-to-hub'
  properties: {
    allowVirtualNetworkAccess: true
    allowForwardedTraffic: false
    remoteVirtualNetwork: {
      id: hubVnet.id
    }
  }
}

// -----------------------------------------------------------------------------
// Outputs — surfaced so a downstream stack update or another workload can
// consume the VNet IDs by name.
// -----------------------------------------------------------------------------

output hubVnetId string = hubVnet.id
output spokeVnetId string = spokeVnet.id
