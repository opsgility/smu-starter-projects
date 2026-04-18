// Foundry hub + project + supporting resources for AI-103 Lesson 3.
// TODOs are inline — students fill them in, test with: az bicep build -f infra/main.bicep.
targetScope = 'resourceGroup'

@description('Location for all resources.')
param location string = resourceGroup().location

@description('Foundry AI Services account name.')
param hubName string

@description('Foundry project (child of the AI Services account) name.')
param projectName string

@description('Unique suffix for globally scoped resources.')
param uniqueSuffix string = uniqueString(resourceGroup().id)

// ---------------------------------------------------------------------------
// TODO 1: Declare an Application Insights resource and a Log Analytics workspace.
//         Required types: Microsoft.OperationalInsights/workspaces (2023-09-01),
//         Microsoft.Insights/components (2020-02-02).
// ---------------------------------------------------------------------------

// ---------------------------------------------------------------------------
// TODO 2: Declare a Storage Account (Microsoft.Storage/storageAccounts 2023-05-01),
//         Standard_LRS, StorageV2, with hierarchical namespace disabled.
//         Name: 'ai103sa${uniqueSuffix}'.
// ---------------------------------------------------------------------------

// ---------------------------------------------------------------------------
// TODO 3: Declare an Azure AI Search service (Microsoft.Search/searchServices 2024-06-01-preview),
//         Basic SKU, replica/partition count = 1.
// ---------------------------------------------------------------------------

// ---------------------------------------------------------------------------
// TODO 4: Declare the Foundry AI Services account (Microsoft.CognitiveServices/accounts
//         2025-04-01-preview), kind='AIServices', sku='S0'. Enable systemAssigned identity
//         and set customSubDomainName = hubName.
// ---------------------------------------------------------------------------

// ---------------------------------------------------------------------------
// TODO 5: Declare a Foundry project (Microsoft.CognitiveServices/accounts/projects
//         2025-04-01-preview) as a child of the AI Services account. Enable systemAssigned
//         identity.
// ---------------------------------------------------------------------------

// ---------------------------------------------------------------------------
// TODO 6: Emit outputs (use @description and output keyword):
//         - foundryEndpoint: 'https://${hubName}.services.ai.azure.com/api/projects/${projectName}'
//         - searchEndpoint
//         - storageAccountName
//         - applicationInsightsConnectionString
// ---------------------------------------------------------------------------
