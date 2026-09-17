// Anchorline Outdoors — a minimal Bicep that GitHub Actions deploys via OIDC federation.

targetScope = 'resourceGroup'

param location string = resourceGroup().location

var suffix = uniqueString(resourceGroup().id, deployment().name)
var storageName = toLower('anchoroidc${substring(suffix, 0, 5)}')

resource sa 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageName
  location: location
  sku: { name: 'Standard_LRS' }
  kind: 'StorageV2'
  tags: { workload: 'anchorline-oidc-demo', deployedBy: 'github-actions-oidc' }
  properties: {
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
    supportsHttpsTrafficOnly: true
  }
}

output storageName string = sa.name
