metadata description = 'TaskForge monitoring module: Log Analytics + App Insights'
param location string
param prefix string

resource law 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: '${prefix}-law'
  location: location
  properties: { sku: { name: 'PerGB2018' }, retentionInDays: 30 }
}

resource ai 'Microsoft.Insights/components@2020-02-02' = {
  name: '${prefix}-ai'
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: law.id
  }
}

output aiConnectionString string = ai.properties.ConnectionString
