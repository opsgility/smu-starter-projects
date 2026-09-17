// Anchorline Outdoors — Key Vault + App Configuration + Web App with references.

targetScope = 'resourceGroup'

@description('Deployment location.')
param location string = resourceGroup().location

@description('Three secrets to seed into Key Vault.')
@secure()
param dbConnectionString string

@secure()
param serviceBusConnectionString string

@secure()
param cognitiveServicesKey string

@description('Common tags.')
param tags object = {
  workload: 'anchorline-secrets-config'
  costcenter: 'anchorline-eng'
}

var suffix = uniqueString(resourceGroup().id)
var kvName    = toLower('kv-anchor-${substring(suffix, 0, 8)}')
var appCfgName = 'appcfg-anchor-${substring(suffix, 0, 6)}'
var planName  = 'plan-anchor-${substring(suffix, 0, 6)}'
var webName   = 'web-anchor-${substring(suffix, 0, 6)}'

// 1. Key Vault
resource kv 'Microsoft.KeyVault/vaults@2024-04-01-preview' = {
  name: kvName
  location: location
  tags: tags
  properties: {
    sku: { family: 'A', name: 'standard' }
    tenantId: subscription().tenantId
    enableRbacAuthorization: true
    enableSoftDelete: true
    softDeleteRetentionInDays: 7
    enablePurgeProtection: true
    publicNetworkAccess: 'Enabled'
    networkAcls: { bypass: 'AzureServices', defaultAction: 'Allow' }
  }
}

// 2. Seed three secrets from @secure params
resource secretDb 'Microsoft.KeyVault/vaults/secrets@2024-04-01-preview' = {
  parent: kv
  name: 'DbConnectionString'
  properties: { value: dbConnectionString, attributes: { enabled: true } }
}

resource secretSb 'Microsoft.KeyVault/vaults/secrets@2024-04-01-preview' = {
  parent: kv
  name: 'ServiceBusConnectionString'
  properties: { value: serviceBusConnectionString, attributes: { enabled: true } }
}

resource secretCog 'Microsoft.KeyVault/vaults/secrets@2024-04-01-preview' = {
  parent: kv
  name: 'CognitiveServicesKey'
  properties: { value: cognitiveServicesKey, attributes: { enabled: true } }
}

// 3. App Configuration with feature flags
resource appCfg 'Microsoft.AppConfiguration/configurationStores@2024-05-01' = {
  name: appCfgName
  location: location
  tags: tags
  sku: { name: 'standard' }
  identity: { type: 'SystemAssigned' }
  properties: { publicNetworkAccess: 'Enabled', disableLocalAuth: false }
}

resource ffPromoBanner 'Microsoft.AppConfiguration/configurationStores/keyValues@2024-05-01' = {
  parent: appCfg
  name: '.appconfig.featureflag~2FAnchorlinePromoBanner'
  properties: {
    contentType: 'application/vnd.microsoft.appconfig.ff+json;charset=utf-8'
    value: '{"id":"AnchorlinePromoBanner","enabled":true,"conditions":{"client_filters":[]}}'
  }
}

// 4. Plan + Web App with Key Vault references and App Config wire-up
resource plan 'Microsoft.Web/serverfarms@2023-12-01' = {
  name: planName
  location: location
  tags: tags
  sku: { name: 'B1', tier: 'Basic' }
  kind: 'linux'
  properties: { reserved: true }
}

resource web 'Microsoft.Web/sites@2023-12-01' = {
  name: webName
  location: location
  tags: tags
  identity: { type: 'SystemAssigned' }
  properties: {
    serverFarmId: plan.id
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'DOTNETCORE|10.0'
      minTlsVersion: '1.2'
      ftpsState: 'Disabled'
      appSettings: [
        { name: 'DbConnectionString',         value: '@Microsoft.KeyVault(VaultName=${kv.name};SecretName=DbConnectionString)' }
        { name: 'ServiceBusConnectionString', value: '@Microsoft.KeyVault(VaultName=${kv.name};SecretName=ServiceBusConnectionString)' }
        { name: 'CognitiveServicesKey',       value: '@Microsoft.KeyVault(VaultName=${kv.name};SecretName=CognitiveServicesKey)' }
        { name: 'APP_CONFIGURATION_ENDPOINT', value: appCfg.properties.endpoint }
      ]
    }
  }
}

// 5. Grant Web App identity Key Vault Secrets User + App Config Data Reader
var kvSecretsUser = subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '4633458b-17de-408a-b874-0445c86b69e6')
var appCfgDataReader = subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '516239f1-63e1-4d78-a4de-a74fb236a071')

resource webKvGrant 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: kv
  name: guid(web.id, kv.id, kvSecretsUser)
  properties: {
    principalId: web.identity.principalId
    principalType: 'ServicePrincipal'
    roleDefinitionId: kvSecretsUser
  }
}

resource webAppCfgGrant 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: appCfg
  name: guid(web.id, appCfg.id, appCfgDataReader)
  properties: {
    principalId: web.identity.principalId
    principalType: 'ServicePrincipal'
    roleDefinitionId: appCfgDataReader
  }
}

output webName string = web.name
output keyVaultName string = kv.name
output appConfigEndpoint string = appCfg.properties.endpoint
