metadata description = 'TaskForge network module: VNet + apps/data/pep subnets'
param location string
param prefix string

resource vnet 'Microsoft.Network/virtualNetworks@2024-01-01' = {
  name: '${prefix}-vnet'
  location: location
  properties: {
    addressSpace: { addressPrefixes: ['10.30.0.0/16'] }
    subnets: [
      { name: 'apps', properties: { addressPrefix: '10.30.1.0/24' } }
      { name: 'data', properties: { addressPrefix: '10.30.2.0/24' } }
      { name: 'pep',  properties: { addressPrefix: '10.30.3.0/24' } }
    ]
  }
}

output vnetId string = vnet.id
output subnetAppsId string = vnet.properties.subnets[0].id
