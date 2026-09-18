// TaskForge landing zone — orchestrator
targetScope = 'subscription'
param env string
param location string = 'eastus2'
param prefix string = 'tf'

resource rg 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: 'rg-taskforge-${env}'
  location: location
}

module net 'br:tfacr.azurecr.io/bicep/network:v1' = {
  scope: rg
  name: 'network'
  params: { location: location, prefix: '${prefix}-${env}' }
}

module kv 'br:tfacr.azurecr.io/bicep/keyvault:v1' = {
  scope: rg
  name: 'keyvault'
  params: { location: location, prefix: '${prefix}-${env}' }
}

module mon 'br:tfacr.azurecr.io/bicep/monitoring:v1' = {
  scope: rg
  name: 'monitoring'
  params: { location: location, prefix: '${prefix}-${env}' }
}

output kvId string = kv.outputs.id
output aiConnectionString string = mon.outputs.aiConnectionString
