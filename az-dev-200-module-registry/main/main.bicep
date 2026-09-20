// Anchorline top-level template consuming registry-published modules.
// After you publish modules to the private registry, swap the local refs for br: refs.

targetScope = 'resourceGroup'

@description('Common name prefix.')
param namePrefix string = 'anchorline'

@description('Deployment location.')
param location string = resourceGroup().location

@description('ACR login server hosting the module registry (e.g. anchoracrXXXXXX.azurecr.io).')
param registryLoginServer string

var suffix = uniqueString(resourceGroup().id)
var storageName = toLower('anchor${substring(suffix, 0, 6)}')
var kvName = toLower('kv-anchor-${substring(suffix, 0, 6)}')
var aiName = '${namePrefix}-ai'
var lawName = '${namePrefix}-law'

var commonTags = {
  workload: 'anchorline-shared'
  costcenter: 'anchorline-eng'
  managedBy: 'bicep-registry'
}

resource law 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: lawName
  location: location
  tags: commonTags
  properties: {
    sku: { name: 'PerGB2018' }
    retentionInDays: 30
  }
}

// Consume registry-published modules. Uncomment br: form once published:
// module storage 'br:${registryLoginServer}/bicep/modules/storage:1.2.0' = { ... }

module storage '../modules/storage/main.bicep' = {
  name: 'storage-module'
  params: {
    name: storageName
    location: location
    skuName: 'Standard_LRS'
    tags: commonTags
  }
}

module keyvault '../modules/keyvault/main.bicep' = {
  name: 'keyvault-module'
  params: {
    name: kvName
    location: location
    tags: commonTags
  }
}

module appinsights '../modules/appinsights/main.bicep' = {
  name: 'appinsights-module'
  params: {
    name: aiName
    location: location
    workspaceResourceId: law.id
    tags: commonTags
  }
}

output storageName string = storage.outputs.name
output keyVaultUri string = keyvault.outputs.vaultUri
output appInsightsConnectionString string = appinsights.outputs.connectionString
