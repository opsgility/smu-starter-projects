using './main.bicep'
param env = 'dev'
param storageAccounts = [
  { purpose: 'orders',  sku: 'Standard_LRS' }
  { purpose: 'catalog', sku: 'Standard_LRS' }
]
