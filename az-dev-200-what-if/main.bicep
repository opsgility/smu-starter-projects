// Anchorline Outdoors — what-if gating demo.
// Same shape as the baseline workload the sandbox ARM deployed; edit the SKU or add resources
// then run 'az deployment group what-if' to see the diff before committing to deploy.

targetScope = 'resourceGroup'

param location string = resourceGroup().location
@allowed(['B1','B2','S1','P1v3']) param planSku string = 'B1'
param tags object = { workload: 'anchorline-what-if', costcenter: 'anchorline-eng' }

var suffix = uniqueString(resourceGroup().id)
var storageName = toLower('anchor${substring(suffix, 0, 6)}')
var planName = 'plan-anchor-${substring(suffix, 0, 6)}'

resource storage 'Microsoft.Storage/storageAccounts@2025-01-01' = {
  name: storageName
  location: location
  tags: tags
  sku: { name: 'Standard_LRS' }
  kind: 'StorageV2'
  properties: {
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
    supportsHttpsTrafficOnly: true
  }
}

resource plan 'Microsoft.Web/serverfarms@2024-11-01' = {
  name: planName
  location: location
  tags: tags
  sku: {
    name: planSku
    tier: planSku == 'B1' || planSku == 'B2' ? 'Basic' : (planSku == 'S1' ? 'Standard' : 'PremiumV3')
  }
  kind: 'linux'
  properties: { reserved: true }
}

output planSkuActual string = plan.sku.name
