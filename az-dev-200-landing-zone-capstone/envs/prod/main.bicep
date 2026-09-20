// Anchorline landing-zone workload — prod, two regions.
// Deploys VNet + Key Vault + Log Analytics + App Insights + SQL + App Service in each region.

targetScope = 'resourceGroup'

@description('Environment name.')
param env string = 'prod'

@description('Primary region.')
param primaryLocation string = 'eastus2'

@description('Secondary region.')
param secondaryLocation string = 'westus3'

@description('Object id of the SQL admin AAD group.')
param sqlAdminObjectId string

@description('SQL admin login (AAD group display name).')
param sqlAdminLogin string = 'anchorline-dba-group'

var namePrefixPri = 'anc-${env}-pri'
var namePrefixSec = 'anc-${env}-sec'

var commonTags = {
  workload: 'anchorline-landing-zone'
  environment: env
  costcenter: 'anchorline-eng'
  managedBy: 'bicep-stacks'
}

// ----- Primary region -----
module netPri '../../modules/network/vnet.bicep' = {
  name: 'net-pri'
  params: { namePrefix: namePrefixPri, location: primaryLocation, tags: commonTags }
}

module monPri '../../modules/monitoring/workspace.bicep' = {
  name: 'mon-pri'
  params: { namePrefix: namePrefixPri, location: primaryLocation, tags: commonTags }
}

module kvPri '../../modules/identity/keyvault.bicep' = {
  name: 'kv-pri'
  params: { namePrefix: namePrefixPri, location: primaryLocation, tags: commonTags }
}

module sqlPri '../../modules/data/sqlserver.bicep' = {
  name: 'sql-pri'
  params: {
    namePrefix: namePrefixPri
    location: primaryLocation
    tags: commonTags
    sqlAdminObjectId: sqlAdminObjectId
    sqlAdminLogin: sqlAdminLogin
  }
}

module appPri '../../modules/app/webapp.bicep' = {
  name: 'app-pri'
  params: {
    namePrefix: namePrefixPri
    location: primaryLocation
    tags: commonTags
    appSettings: [
      { name: 'APPLICATIONINSIGHTS_CONNECTION_STRING', value: monPri.outputs.appInsightsConnectionString }
      { name: 'KEY_VAULT_URI', value: kvPri.outputs.vaultUri }
      { name: 'SQL_SERVER_FQDN', value: sqlPri.outputs.serverFqdn }
    ]
  }
}

// ----- Secondary region -----
module netSec '../../modules/network/vnet.bicep' = {
  name: 'net-sec'
  params: { namePrefix: namePrefixSec, location: secondaryLocation, addressPrefix: '10.101.0.0/16', tags: commonTags }
}

module monSec '../../modules/monitoring/workspace.bicep' = {
  name: 'mon-sec'
  params: { namePrefix: namePrefixSec, location: secondaryLocation, tags: commonTags }
}

module kvSec '../../modules/identity/keyvault.bicep' = {
  name: 'kv-sec'
  params: { namePrefix: namePrefixSec, location: secondaryLocation, tags: commonTags }
}

module sqlSec '../../modules/data/sqlserver.bicep' = {
  name: 'sql-sec'
  params: {
    namePrefix: namePrefixSec
    location: secondaryLocation
    tags: commonTags
    sqlAdminObjectId: sqlAdminObjectId
    sqlAdminLogin: sqlAdminLogin
  }
}

module appSec '../../modules/app/webapp.bicep' = {
  name: 'app-sec'
  params: {
    namePrefix: namePrefixSec
    location: secondaryLocation
    tags: commonTags
    appSettings: [
      { name: 'APPLICATIONINSIGHTS_CONNECTION_STRING', value: monSec.outputs.appInsightsConnectionString }
      { name: 'KEY_VAULT_URI', value: kvSec.outputs.vaultUri }
      { name: 'SQL_SERVER_FQDN', value: sqlSec.outputs.serverFqdn }
    ]
  }
}

output primaryWebUrl string = appPri.outputs.webUrl
output secondaryWebUrl string = appSec.outputs.webUrl
