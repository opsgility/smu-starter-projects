// Anchorline Outdoors — the workload to manage as a deployment stack.
// Storage + Plan + Web App running .NET 10. Same shape as the M5L10 baseline sandbox.

targetScope = 'resourceGroup'

param location string = resourceGroup().location
param tags object = { workload: 'anchorline-stack-demo', costcenter: 'anchorline-eng' }

var suffix = uniqueString(resourceGroup().id)
var storageName = toLower('anchor${substring(suffix, 0, 6)}')
var planName = 'plan-anchor-${substring(suffix, 0, 6)}'
var webName = 'web-anchor-${substring(suffix, 0, 6)}'

resource storage 'Microsoft.Storage/storageAccounts@2023-05-01' = {
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

resource plan 'Microsoft.Web/serverfarms@2023-12-01' = {
  name: planName
  location: location
  tags: tags
  sku: { name: 'B1', tier: 'Basic' }
  kind: 'linux'
  properties: { reserved: true }
}

resource web 'Microsoft.Web/sites@2023-12-01' = {
  name: webName
  location: location
  tags: tags
  identity: { type: 'SystemAssigned' }
  properties: {
    serverFarmId: plan.id
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'DOTNETCORE|10.0'
      minTlsVersion: '1.2'
      ftpsState: 'Disabled'
    }
  }
}

output webName string = web.name
output storageName string = storage.name
