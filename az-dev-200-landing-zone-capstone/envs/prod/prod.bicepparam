using './main.bicep'
param env = 'prod'
param primaryLocation = 'eastus2'
param secondaryLocation = 'westus3'
param sqlAdminObjectId = readEnvironmentVariable('SQL_ADMIN_OBJECT_ID', '00000000-0000-0000-0000-000000000000')
param sqlAdminLogin = 'anchorline-dba-group'
