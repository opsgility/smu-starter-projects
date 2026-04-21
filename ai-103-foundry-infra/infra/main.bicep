@description('Azure region for all resources')
param location string = 'eastus2'

@description('Name of the Foundry AI Services (hub) account')
param hubName string

@description('Name of the Foundry project (child of hub)')
param projectName string

// uniqueSuffix is used to avoid global name collisions on storage + search
var uniqueSuffix = toLower(uniqueString(resourceGroup().id))

// TODO 1 (Exercise 1 Step 4): Declare Log Analytics workspace + App Insights
//   - Log Analytics: Microsoft.OperationalInsights/workspaces@2023-09-01
//       name: 'ai103-la-${uniqueSuffix}', sku PerGB2018, retentionInDays 30
//   - App Insights: Microsoft.Insights/components@2020-02-02
//       name: 'ai103-ai-${uniqueSuffix}', kind 'web', WorkspaceResourceId -> la.id

// TODO 2 (Exercise 1 Step 5): Declare the Storage account
//   - Microsoft.Storage/storageAccounts@2023-05-01
//       name: 'ai103sa${uniqueSuffix}', kind StorageV2, sku Standard_LRS
//       allowBlobPublicAccess false, minimumTlsVersion TLS1_2, isHnsEnabled false

// TODO 3 (Exercise 1 Step 6): Declare Azure AI Search
//   - Microsoft.Search/searchServices@2024-06-01-preview
//       name: 'ai103search${uniqueSuffix}', sku basic
//       replicaCount 1, partitionCount 1, hostingMode default
//       authOptions: aadOrApiKey with aadAuthFailureMode http403

// TODO 4 (Exercise 1 Step 7): Declare the Foundry AI Services account (the hub)
//   - Microsoft.CognitiveServices/accounts@2025-04-01-preview
//       name: hubName, kind 'AIServices', sku S0
//       identity: SystemAssigned
//       customSubDomainName: hubName, publicNetworkAccess Enabled, disableLocalAuth false

// TODO 5 (Exercise 1 Step 8): Declare the Foundry project as a child of the hub
//   - Microsoft.CognitiveServices/accounts/projects@2025-04-01-preview
//       parent: hub, name: projectName, location: location
//       identity: SystemAssigned, properties: {}

// TODO 6 (Exercise 1 Step 9): Emit outputs
//   - foundryEndpoint string = 'https://${hubName}.services.ai.azure.com/api/projects/${projectName}'
//   - searchEndpoint string = 'https://${search.name}.search.windows.net'
//   - storageAccountName string = storage.name
//   - applicationInsightsConnectionString string = appInsights.properties.ConnectionString
