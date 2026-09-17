// Dev is a single-region trim of prod. Reuses the same modules.
targetScope = 'resourceGroup'
param env string = 'dev'
param location string = 'eastus2'
param sqlAdminObjectId string
param sqlAdminLogin string = 'anchorline-dba-group'

var namePrefix = 'anc-${env}'
var tags = { workload: 'anchorline-landing-zone', environment: env, costcenter: 'anchorline-eng' }

module net '../../modules/network/vnet.bicep' = {
  name: 'net'
  params: { namePrefix: namePrefix, location: location, tags: tags }
}

module mon '../../modules/monitoring/workspace.bicep' = {
  name: 'mon'
  params: { namePrefix: namePrefix, location: location, tags: tags, retentionDays: 7 }
}

module kv '../../modules/identity/keyvault.bicep' = {
  name: 'kv'
  params: { namePrefix: namePrefix, location: location, tags: tags }
}

module sql '../../modules/data/sqlserver.bicep' = {
  name: 'sql'
  params: {
    namePrefix: namePrefix
    location: location
    tags: tags
    sqlAdminObjectId: sqlAdminObjectId
    sqlAdminLogin: sqlAdminLogin
  }
}

module app '../../modules/app/webapp.bicep' = {
  name: 'app'
  params: {
    namePrefix: namePrefix
    location: location
    tags: tags
    skuName: 'B1'
    appSettings: [
      { name: 'APPLICATIONINSIGHTS_CONNECTION_STRING', value: mon.outputs.appInsightsConnectionString }
      { name: 'KEY_VAULT_URI', value: kv.outputs.vaultUri }
    ]
  }
}

output webUrl string = app.outputs.webUrl
