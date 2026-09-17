using './main.bicep'
param env = 'prod'
param storageAccounts = [
  { purpose: 'orders',    sku: 'Standard_GRS' }
  { purpose: 'catalog',   sku: 'Standard_GRS' }
  { purpose: 'telemetry', sku: 'Standard_GRS' }
  { purpose: 'audit',     sku: 'Standard_ZRS' }
]
