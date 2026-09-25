// SMU-BICEP-FUND Lab 06 — starter main.bicep
//
// State at Exercise 1 baseline: ONE Ubuntu VM, ONE NIC, ONE public IP, hard-wired
// names, deployed at RG scope. Everything is single-instance and copy-and-paste
// duplicated — no loops. You will refactor this in place across Exercises 1-3:
//
//   Ex 1 — replace the single VM + NIC with a copy-loop that deploys `vmCount`
//          Ubuntu VMs (allowed range 1-5). Same shape (Standard_B1s, Standard_LRS
//          OS disk, Ubuntu 22.04). The NIC loop must match the VM loop.
//   Ex 2 — replace the always-on public IP with a CONDITIONAL loop that only
//          deploys a PIP for VM index 0. Attach the PIP to NIC 0 only; NICs 1..N
//          have no public IP.
//   Ex 3 — add a role assignment at RG scope granting the built-in Reader role
//          (roleDefinitionId acdd72a7-3385-48ef-bd42-f606fba81ae7) to the
//          service-principal object ID passed in via `readerPrincipalId`.
//
// Ex 4 and Ex 5 move to policy.bicep (sub-scope). This file stays RG-scope.

targetScope = 'resourceGroup'

// -----------------------------------------------------------------------------
// Parameters
// -----------------------------------------------------------------------------

@description('Azure region for all resources. Defaults to the RG location.')
param location string = resourceGroup().location

@description('Tag applied to all resources for cost + ownership tracking.')
param workload string = 'cascade-lab06'

@description('How many identical Ubuntu VMs to deploy in the copy loop.')
@minValue(1)
@maxValue(5)
param vmCount int = 2

@description('VM admin username. Never hard-code in Production — pass via CLI.')
param adminUsername string = 'cascadeadmin'

@description('VM admin password. Pass via -p secure prompt; do not commit.')
@secure()
param adminPassword string

@description('Service principal (or user) object ID that will receive the Reader role on this RG in Exercise 3.')
param readerPrincipalId string = ''

// -----------------------------------------------------------------------------
// Shared network (a single /24 VNet + subnet — no loop; every NIC hangs off it)
// -----------------------------------------------------------------------------

resource vnet 'Microsoft.Network/virtualNetworks@2024-05-01' = {
  name: '${workload}-vnet'
  location: location
  tags: {
    workload: workload
    lesson: 'lab06-loops-scopes'
  }
  properties: {
    addressSpace: {
      addressPrefixes: [
        '10.60.0.0/16'
      ]
    }
    subnets: [
      {
        name: 'vm-subnet'
        properties: {
          addressPrefix: '10.60.1.0/24'
        }
      }
    ]
  }
}

// -----------------------------------------------------------------------------
// Exercise 1 baseline — one hard-wired PIP, one NIC, one VM.
// Refactor this section into copy loops (VM loop + matching NIC loop).
// -----------------------------------------------------------------------------

resource pip0 'Microsoft.Network/publicIPAddresses@2024-05-01' = {
  name: '${workload}-pip-0'
  location: location
  sku: {
    name: 'Standard'
  }
  properties: {
    publicIPAllocationMethod: 'Static'
  }
}

resource nic0 'Microsoft.Network/networkInterfaces@2024-05-01' = {
  name: '${workload}-nic-0'
  location: location
  properties: {
    ipConfigurations: [
      {
        name: 'ipconfig1'
        properties: {
          privateIPAllocationMethod: 'Dynamic'
          subnet: {
            id: '${vnet.id}/subnets/vm-subnet'
          }
          publicIPAddress: {
            id: pip0.id
          }
        }
      }
    ]
  }
}

resource vm0 'Microsoft.Compute/virtualMachines@2024-11-01' = {
  name: '${workload}-vm-0'
  location: location
  properties: {
    hardwareProfile: {
      vmSize: 'Standard_B1s'
    }
    storageProfile: {
      imageReference: {
        publisher: 'Canonical'
        offer: '0001-com-ubuntu-server-jammy'
        sku: '22_04-lts-gen2'
        version: 'latest'
      }
      osDisk: {
        createOption: 'FromImage'
        managedDisk: {
          storageAccountType: 'Standard_LRS'
        }
      }
    }
    networkProfile: {
      networkInterfaces: [
        {
          id: nic0.id
        }
      ]
    }
    osProfile: {
      computerName: '${workload}-vm-0'
      adminUsername: adminUsername
      adminPassword: adminPassword
      linuxConfiguration: {
        disablePasswordAuthentication: false
      }
    }
  }
}

// -----------------------------------------------------------------------------
// Exercise 3 will add a Microsoft.Authorization/roleAssignments@2022-04-01
// scoped to this RG that grants Reader to `readerPrincipalId`. Use guid() with
// the RG id + principalId + roleDefinitionId to make the assignment name
// deterministic. Do NOT add it now — Exercise 3 walks you through it.
// -----------------------------------------------------------------------------
