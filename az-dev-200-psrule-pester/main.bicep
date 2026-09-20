// Anchorline Outdoors — a Storage + Plan template we deliberately test with PSRule + Pester.

targetScope = 'resourceGroup'

param location string = resourceGroup().location

var suffix = uniqueString(resourceGroup().id)
var storageName = toLower('anchor${substring(suffix, 0, 6)}')

resource sa 'Microsoft.Storage/storageAccounts@2025-01-01' = {
  name: storageName
  location: location
  sku: { name: 'Standard_LRS' }
  kind: 'StorageV2'
  tags: {
    workload: 'anchorline-testing'
    costcenter: 'anchorline-eng'
    owner: 'platform-team'
    environment: 'dev'
  }
  properties: {
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
    supportsHttpsTrafficOnly: true
    accessTier: 'Hot'
  }
}

output storageName string = sa.name
