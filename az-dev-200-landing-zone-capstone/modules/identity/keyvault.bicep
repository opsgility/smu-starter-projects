// Anchorline landing zone — Key Vault with RBAC authorization.
param namePrefix string
param location string
param tags object = {}

var kvName = '${substring(replace(namePrefix, '-', ''), 0, min(length(replace(namePrefix, '-', '')), 12))}-kv-${uniqueString(resourceGroup().id, namePrefix)}'
var kvNameSanitized = toLower(substring(kvName, 0, min(24, length(kvName))))

resource kv 'Microsoft.KeyVault/vaults@2024-11-01' = {
  name: kvNameSanitized
  location: location
  tags: tags
  properties: {
    sku: { family: 'A', name: 'standard' }
    tenantId: subscription().tenantId
    enableRbacAuthorization: true
    enableSoftDelete: true
    softDeleteRetentionInDays: 7
    enablePurgeProtection: true
  }
}

output vaultUri string = kv.properties.vaultUri
output vaultId string = kv.id
