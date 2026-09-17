// Anchorline Outdoors — loops, conditionals, and 'existing' patterns.
// Drives N storage accounts from an array parameter, conditionally deploys a Key Vault
// (prod only), and injects a subnet into an existing VNet without redeploying it.

targetScope = 'resourceGroup'

@description('Environment name; drives conditional deployments.')
@allowed(['dev', 'test', 'prod'])
param env string

@description('Deployment location.')
param location string = resourceGroup().location

@description('Array of storage account definitions to deploy in one loop.')
param storageAccounts array = [
  { purpose: 'orders',    sku: 'Standard_LRS' }
  { purpose: 'catalog',   sku: 'Standard_LRS' }
  { purpose: 'telemetry', sku: 'Standard_GRS' }
]

@description('Existing VNet name to receive a new subnet.')
param existingVnetName string = 'vnet-anchorline-existing'

@description('Existing VNet resource group; defaults to current RG.')
param existingVnetRg string = resourceGroup().name

@description('Common tags.')
param tags object = {
  workload: 'anchorline-multi-env'
  environment: env
  costcenter: 'anchorline-eng'
}

var suffix = uniqueString(resourceGroup().id, env)

resource storages 'Microsoft.Storage/storageAccounts@2023-05-01' = [for (sa, i) in storageAccounts: {
  name: toLower('anchor${sa.purpose}${substring(suffix, 0, 5)}')
  location: location
  tags: union(tags, { purpose: sa.purpose })
  sku: { name: sa.sku }
  kind: 'StorageV2'
  properties: {
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
    supportsHttpsTrafficOnly: true
  }
}]

// Prod-only Key Vault
resource kvProd 'Microsoft.KeyVault/vaults@2024-04-01-preview' = if (env == 'prod') {
  name: toLower('kv-anchor-${substring(suffix, 0, 8)}')
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

// Reference existing VNet — no redeploy.
resource vnet 'Microsoft.Network/virtualNetworks@2024-01-01' existing = {
  name: existingVnetName
  scope: resourceGroup(existingVnetRg)
}

// Inject a new subnet into the existing VNet.
resource newSubnet 'Microsoft.Network/virtualNetworks/subnets@2024-01-01' = {
  parent: vnet
  name: 'snet-${env}-workload'
  properties: {
    addressPrefix: env == 'prod' ? '10.42.10.0/24' : '10.42.20.0/24'
    privateEndpointNetworkPolicies: 'Enabled'
    privateLinkServiceNetworkPolicies: 'Enabled'
  }
}

output storageAccountCount int = length(storages)
output storageNames array = [for (sa, i) in storageAccounts: storages[i].name]
output prodKeyVaultDeployed bool = env == 'prod'
output newSubnetId string = newSubnet.id
