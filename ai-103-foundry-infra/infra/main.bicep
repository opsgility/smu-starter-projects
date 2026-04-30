@description('Azure region for all resources')
param location string = 'eastus2'

@description('Name of the Foundry project (child of hub)')
param projectName string

// uniqueSuffix ensures globally unique names for resources with global namespaces
var uniqueSuffix = toLower(uniqueString(resourceGroup().id))

// hubName must be globally unique — derive it from uniqueSuffix like storage and search
var hubName = 'ai103hub${uniqueSuffix}'

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
