// Anchorline dev environment — small SKUs, low redundancy.
targetScope = 'resourceGroup'
param location string = resourceGroup().location

var suffix = uniqueString(resourceGroup().id, 'dev')

resource sa 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: toLower('anchordev${substring(suffix, 0, 6)}')
  location: location
  sku: { name: 'Standard_LRS' }
  kind: 'StorageV2'
  tags: { environment: 'dev', workload: 'anchorline-multi-env' }
  properties: {
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
    supportsHttpsTrafficOnly: true
  }
}

output storageName string = sa.name
