@description('Azure region for all resources')
param location string = 'eastus2'

@description('Name of the Foundry AI Services (hub) account')
param hubName string

@description('Name of the Foundry project (child of hub)')
param projectName string

// uniqueSuffix is used to avoid global name collisions on storage + search
var uniqueSuffix = toLower(uniqueString(resourceGroup().id))

// Exercise 1 - Step 3 Start
// Exercise 1 - Step 3 End

// Exercise 1 - Step 4 Start
// Exercise 1 - Step 4 End

// Exercise 1 - Step 5 Start
// Exercise 1 - Step 5 End

// Exercise 1 - Step 6 Start
// Exercise 1 - Step 6 End

// Exercise 1 - Step 7 Start
// Exercise 1 - Step 7 End

// Exercise 1 - Step 8 Start
// Exercise 1 - Step 8 End
