// Anchorline Outdoors — first Bicep template
// Provisions a Storage Account, App Service Plan (Linux, B1), and Web App running .NET 10.
// Target scope: resource group.

targetScope = 'resourceGroup'

@description('Name prefix for the web app; a 6-char unique suffix will be appended.')
@minLength(3)
@maxLength(20)
param appName string = 'anchor-web'

@description('Deployment location. Defaults to the resource group location.')
param location string = resourceGroup().location

@description('App Service Plan SKU.')
@allowed([
  'B1'
  'B2'
  'S1'
  'P1v3'
])
param sku string = 'B1'

@description('Tags applied to every resource.')
param tags object = {
  workload: 'anchorline-storefront'
  costcenter: 'anchorline-eng'
  owner: 'platform-team'
}

var suffix = uniqueString(resourceGroup().id, appName)
var storageName = toLower('anchor${substring(suffix, 0, 6)}')
var planName = 'plan-${appName}'
var webName = '${appName}-${substring(suffix, 0, 6)}'

resource storage 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  tags: tags
  properties: {
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
    supportsHttpsTrafficOnly: true
  }
}

resource plan 'Microsoft.Web/serverfarms@2023-12-01' = {
  name: planName
  location: location
  sku: {
    name: sku
    tier: sku == 'B1' || sku == 'B2' ? 'Basic' : (sku == 'S1' ? 'Standard' : 'PremiumV3')
  }
  kind: 'linux'
  tags: tags
  properties: {
    reserved: true
  }
}

resource web 'Microsoft.Web/sites@2023-12-01' = {
  name: webName
  location: location
  tags: tags
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    serverFarmId: plan.id
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'DOTNETCORE|10.0'
      minTlsVersion: '1.2'
      ftpsState: 'Disabled'
      alwaysOn: sku != 'B1'
      appSettings: [
        {
          name: 'WEBSITE_RUN_FROM_PACKAGE'
          value: '1'
        }
        {
          name: 'STORAGE_ACCOUNT'
          value: storage.name
        }
      ]
    }
  }
}

output webAppName string = web.name
output webAppUrl string = 'https://${web.properties.defaultHostName}'
output storageAccountName string = storage.name
output servicePlanId string = plan.id
