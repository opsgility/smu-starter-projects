// Creates a user-assigned managed identity and grants it Azure AI User on the Foundry project.
targetScope = 'resourceGroup'

@description('Location for the identity.')
param location string = resourceGroup().location

@description('Name of the user-assigned managed identity.')
param identityName string = 'ai103-chat-mi'

@description('Foundry AI Services account (hub) name.')
param hubName string

// ---------------------------------------------------------------------------
// TODO 1: Create a Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31 resource
//         named `identityName` in `location`.
// ---------------------------------------------------------------------------

// ---------------------------------------------------------------------------
// TODO 2: Look up the existing Foundry AI Services account as an existing resource
//         so we can scope the role assignment to it.
// ---------------------------------------------------------------------------

// ---------------------------------------------------------------------------
// TODO 3: Assign the "Azure AI User" built-in role (roleDefinitionId
//         53ca6127-db72-4b80-b1b0-d745d6d5456d) to the managed identity at the AI Services
//         scope. Use Microsoft.Authorization/roleAssignments@2022-04-01.
//         Hint: guid(resourceId(...), identityName, 'Azure AI User') for the role
//         assignment name.
// ---------------------------------------------------------------------------

output identityClientId string = '<TODO: reference the managed identity clientId>'
output identityPrincipalId string = '<TODO: reference the managed identity principalId>'
