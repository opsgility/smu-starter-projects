// Anchorline prod environment — GRS redundancy, denied public blob, standard security posture.
targetScope = 'resourceGroup'
param location string = resourceGroup().location
var suffix = uniqueString(resourceGroup().id, 'prod')

resource sa 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: toLower('anchorprod${substring(suffix, 0, 6)}')
  location: location
  sku: { name: 'Standard_GRS' }
  kind: 'StorageV2'
  tags: { environment: 'prod', workload: 'anchorline-multi-env' }
  properties: {
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
    allowSharedKeyAccess: false
    supportsHttpsTrafficOnly: true
  }
}

output storageName string = sa.name
