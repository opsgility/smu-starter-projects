// Anchorline landing zone — hub-and-spoke VNet module.
param namePrefix string
param location string
param addressPrefix string = '10.100.0.0/16'
param tags object = {}

var vnetName = '${namePrefix}-vnet'

resource vnet 'Microsoft.Network/virtualNetworks@2024-01-01' = {
  name: vnetName
  location: location
  tags: tags
  properties: {
    addressSpace: { addressPrefixes: [ addressPrefix ] }
    subnets: [
      { name: 'snet-app',      properties: { addressPrefix: cidrSubnet(addressPrefix, 24, 0) } }
      { name: 'snet-data',     properties: { addressPrefix: cidrSubnet(addressPrefix, 24, 1) } }
      { name: 'snet-private-endpoints', properties: { addressPrefix: cidrSubnet(addressPrefix, 24, 2) } }
    ]
  }
}

output vnetId string = vnet.id
output vnetName string = vnet.name
output appSubnetId string = '${vnet.id}/subnets/snet-app'
