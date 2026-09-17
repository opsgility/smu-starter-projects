// Anchorline shared module — storage account.
// Version: 1.2.0 (semver bumps published to the registry).

@description('Storage account name; must be globally unique, 3-24 lowercase alphanumeric.')
@minLength(3)
@maxLength(24)
param name string

@description('Deployment location.')
param location string

@description('SKU name; Standard_LRS default; use Standard_GRS for prod.')
@allowed([
  'Standard_LRS'
  'Standard_GRS'
  'Standard_RAGRS'
  'Standard_ZRS'
  'Premium_LRS'
])
param skuName string = 'Standard_LRS'

@description('Common tags.')
param tags object = {}

resource sa 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: name
  location: location
  tags: tags
  sku: { name: skuName }
  kind: 'StorageV2'
  properties: {
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
    supportsHttpsTrafficOnly: true
    accessTier: 'Hot'
  }
}

output name string = sa.name
output id string = sa.id
output primaryBlobEndpoint string = sa.properties.primaryEndpoints.blob
