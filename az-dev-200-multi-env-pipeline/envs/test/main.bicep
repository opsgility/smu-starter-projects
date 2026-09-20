// Anchorline test environment — matches prod topology at lower SKU.
targetScope = 'resourceGroup'
param location string = resourceGroup().location
var suffix = uniqueString(resourceGroup().id, 'test')

resource sa 'Microsoft.Storage/storageAccounts@2025-01-01' = {
  name: toLower('anchortest${substring(suffix, 0, 6)}')
  location: location
  sku: { name: 'Standard_ZRS' }
  kind: 'StorageV2'
  tags: { environment: 'test', workload: 'anchorline-multi-env' }
  properties: {
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
    supportsHttpsTrafficOnly: true
  }
}

output storageName string = sa.name
