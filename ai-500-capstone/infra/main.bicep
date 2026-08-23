// azd infra shim — the lab's ARM template already provisioned Foundry, Container Apps env,
// ACR, and App Insights. azd deploy only needs the target names, which come from `azd env`.
// This file exists so `azd up` and `azd deploy` are happy in the capstone; the actual
// resource-creation is done by the SkillMeUp platform template attached to the lab.

targetScope = 'resourceGroup'

param environmentName string
param location string = resourceGroup().location

// The lab pre-creates these; azd resolves them by name via `azd env set`.
param containerAppName string
param containerAppEnvName string
param acrLoginServer string
param applicationInsightsConnectionString string
param foundryProjectEndpoint string
param foundryModel string

output CONTAINER_APP_NAME string = containerAppName
output CONTAINER_APP_ENV string = containerAppEnvName
output ACR_LOGIN_SERVER string = acrLoginServer
output APPLICATIONINSIGHTS_CONNECTION_STRING string = applicationInsightsConnectionString
output FOUNDRY_PROJECT_ENDPOINT string = foundryProjectEndpoint
output FOUNDRY_MODEL string = foundryModel
output AZURE_LOCATION string = location
output AZURE_ENV_NAME string = environmentName
