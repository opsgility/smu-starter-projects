// Anchorline shared module — Application Insights workspace-based.
// Version: 1.0.0.

@description('Application Insights resource name.')
param name string

@description('Log Analytics workspace resource id (workspace-based AI).')
param workspaceResourceId string

@description('Deployment location.')
param location string

@description('Common tags.')
param tags object = {}

resource ai 'Microsoft.Insights/components@2020-02-02' = {
  name: name
  location: location
  tags: tags
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: workspaceResourceId
    IngestionMode: 'LogAnalytics'
    publicNetworkAccessForIngestion: 'Enabled'
    publicNetworkAccessForQuery: 'Enabled'
  }
}

output name string = ai.name
output instrumentationKey string = ai.properties.InstrumentationKey
output connectionString string = ai.properties.ConnectionString
