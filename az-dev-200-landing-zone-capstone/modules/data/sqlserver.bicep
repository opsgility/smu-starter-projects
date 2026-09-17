// Anchorline landing zone — Azure SQL logical server + one database with Entra admin.
param namePrefix string
param location string
param tags object = {}
param sqlAdminObjectId string
param sqlAdminLogin string

var serverName = toLower('${namePrefix}-sql-${uniqueString(resourceGroup().id, namePrefix)}')
var dbName = 'anchorline-db'

resource sql 'Microsoft.Sql/servers@2023-08-01-preview' = {
  name: serverName
  location: location
  tags: tags
  identity: { type: 'SystemAssigned' }
  properties: {
    administrators: {
      administratorType: 'ActiveDirectory'
      login: sqlAdminLogin
      sid: sqlAdminObjectId
      tenantId: subscription().tenantId
      azureADOnlyAuthentication: true
      principalType: 'Group'
    }
    minimalTlsVersion: '1.2'
    publicNetworkAccess: 'Enabled'
    version: '12.0'
  }
}

resource db 'Microsoft.Sql/servers/databases@2023-08-01-preview' = {
  parent: sql
  name: dbName
  location: location
  tags: tags
  sku: { name: 'GP_S_Gen5', tier: 'GeneralPurpose', family: 'Gen5', capacity: 1 }
  properties: {
    collation: 'SQL_Latin1_General_CP1_CI_AS'
    autoPauseDelay: 60
    minCapacity: json('0.5')
    maxSizeBytes: 34359738368
    zoneRedundant: false
  }
}

output serverFqdn string = sql.properties.fullyQualifiedDomainName
output databaseName string = db.name
