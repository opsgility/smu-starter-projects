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
// Exercise 2 - Step 3 Start
// Exercise 2 - Step 3 End

// -----------------------------------------------------------------------------
// Exercise 2 - Step 4 Start
// Exercise 2 - Step 4 End

// -----------------------------------------------------------------------------
// Exercise 2 - Step 5 Start
// Exercise 2 - Step 5 End

// -----------------------------------------------------------------------------
// Outputs — Exercise 3 pulls these to drive AZURE_CLIENT_ID and verify the
// role assignment landed against the correct principal.
// -----------------------------------------------------------------------------

// Exercise 2 - Step 6 Start
output identityClientId string = ''
output identityPrincipalId string = ''
// Exercise 2 - Step 6 End
