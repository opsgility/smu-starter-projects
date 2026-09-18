// Anchorline landing zone — App Service Plan + Linux Web App running .NET 10.
param namePrefix string
param location string
param tags object = {}
param appSettings array = []
param skuName string = 'P1v3'

var planName = '${namePrefix}-plan'
var webName = '${namePrefix}-web'

resource plan 'Microsoft.Web/serverfarms@2024-11-01' = {
  name: planName
  location: location
  tags: tags
  sku: { name: skuName, tier: 'PremiumV3' }
  kind: 'linux'
  properties: { reserved: true }
}

resource web 'Microsoft.Web/sites@2024-11-01' = {
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
      alwaysOn: true
      appSettings: appSettings
    }
  }
}

output webName string = web.name
output webUrl string = 'https://${web.properties.defaultHostName}'
output webPrincipalId string = web.identity.principalId
