// bicep/identity.bicep
// Summitline Outfitters — user-assigned managed identity + Azure AI User role
// assignment on the pre-deployed Foundry AI Services account (hub).
//
// Exercise 2 of Lab 2258 (AI-103 Lesson 4) walks you through filling in the
// three TODOs below and wiring up the two outputs at the bottom of the file.

@description('Azure region for the user-assigned managed identity. Policy 986 enforces eastus2 for AI-103 labs.')
param location string = resourceGroup().location

@description('Name of the user-assigned managed identity to create.')
param identityName string = 'summitline-concierge-mi'

@description('Name of the pre-deployed Foundry AI Services account (hub) that the role assignment targets. Pass the foundryAccountName output from the baseline ARM deployment.')
param hubName string

// -----------------------------------------------------------------------------
// TODO 1 (Exercise 2 Step 3): Declare the user-assigned managed identity.
//
// Create a resource of type
//   Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31
// named `mi`, using the `identityName` and `location` parameters above.
// -----------------------------------------------------------------------------


// -----------------------------------------------------------------------------
// TODO 2 (Exercise 2 Step 4): Reference the existing Foundry hub.
//
// Add a resource of type
//   Microsoft.CognitiveServices/accounts@2025-04-01-preview
// named `hub`, using the `existing` keyword and the `hubName` parameter.
// We do NOT want Bicep to re-create the hub — the baseline ARM deployment
// already provisioned it in Exercise 1. We only need a handle so the role
// assignment below can target its scope.
// -----------------------------------------------------------------------------


// -----------------------------------------------------------------------------
// TODO 3 (Exercise 2 Step 5): Grant the managed identity the Azure AI User
// built-in role on the hub scope.
//
// Built-in role ID for Azure AI User:
//   53ca6127-db72-4b80-b1b0-d745d6d5456d
//
// Add a resource of type
//   Microsoft.Authorization/roleAssignments@2022-04-01
// with:
//   - name: guid(hub.id, mi.id, 'Azure AI User')  // deterministic + idempotent
//   - scope: hub
//   - properties.roleDefinitionId: subscriptionResourceId(
//       'Microsoft.Authorization/roleDefinitions', azureAiUserRoleId)
//   - properties.principalId: mi.properties.principalId   // NOT mi.id
//   - properties.principalType: 'ServicePrincipal'        // avoids Entra propagation 400s
// -----------------------------------------------------------------------------


// -----------------------------------------------------------------------------
// Outputs — Exercise 3 pulls these to drive AZURE_CLIENT_ID and verify the
// role assignment landed against the correct principal.
// -----------------------------------------------------------------------------

// TODO (Exercise 2 Step 6): Emit the UAMI's clientId (NOT mi.id).
output identityClientId string = ''

// TODO (Exercise 2 Step 6): Emit the UAMI's principalId (NOT mi.id).
output identityPrincipalId string = ''
