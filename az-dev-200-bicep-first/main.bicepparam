// Parameter file for main.bicep — Anchorline dev environment.
using './main.bicep'

param appName = 'anchor-web'
param sku = 'B1'
param tags = {
  workload: 'anchorline-storefront'
  costcenter: 'anchorline-eng'
  owner: 'platform-team'
  environment: 'dev'
}
