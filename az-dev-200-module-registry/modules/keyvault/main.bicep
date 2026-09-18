// Anchorline shared module — Key Vault.
// Version: 1.0.0.

@description('Key Vault name; must be globally unique, 3-24 alphanumeric+hyphen.')
@minLength(3)
@maxLength(24)
param name string

@description('Deployment location.')
param location string

@description('Enable RBAC authorization mode (recommended over access policies).')
param enableRbacAuthorization bool = true

@description('Tenant id.')
param tenantId string = subscription().tenantId

@description('Common tags.')
param tags object = {}

resource kv 'Microsoft.KeyVault/vaults@2024-11-01' = {
  name: name
  location: location
  tags: tags
  properties: {
    sku: { family: 'A', name: 'standard' }
    tenantId: tenantId
    enableRbacAuthorization: enableRbacAuthorization
    enablePurgeProtection: true
    enableSoftDelete: true
    softDeleteRetentionInDays: 7
    publicNetworkAccess: 'Enabled'
    networkAcls: {
      bypass: 'AzureServices'
      defaultAction: 'Allow'
    }
  }
}

output name string = kv.name
output id string = kv.id
output vaultUri string = kv.properties.vaultUri
