# TaskForge DR Runbook — eastus2 → centralus

## Trigger criteria
- Azure Service Health reports eastus2 outage affecting App Service / SQL / Cosmos for > 15 min with no ETA
- OR Front Door health probes to eastus2 App Service fail > 3 min

## Prerequisites (verify quarterly)
- centralus SQL failover-group secondary is < 5 min behind
- centralus Cosmos secondary is < 5 min behind
- centralus App Service prod slot has last-known-good build
- centralus SB namespace is receiving message replication

## Failover steps (target RTO 30 min)

1. [1 min] Post to `#taskforge-incidents`: "Initiating DR failover eastus2 → centralus. RTO 30 min. All hands."
2. [3 min] `az sql failover-group set-primary --name tf-fog --resource-group rg-taskforge-prod --server tf-sql-centralus-<suffix>`
3. [2 min] `az cosmosdb failover-priority-change --name tf-cos-<suffix> --resource-group rg-taskforge-prod --failover-policies "centralus=0" "eastus2=1"`
4. [2 min] Update Front Door origin group to prefer centralus
5. [5 min] Verify centralus App Service: `curl -f https://taskforge.anchorline.com/health/ready`
6. [5 min] Run DR smoke tests: create task, update, delete, SignalR broadcast
7. [10 min] Post to customer status page: "DR complete; TaskForge is serving from centralus."

## Failback (when eastus2 is back)
1. Sync eastus2 from centralus (SQL failover-group flip, Cosmos priority flip)
2. Front Door origin group back to eastus2
3. Verify

## Contacts
- Primary on-call: platform@anchorline.local
- Escalation: cto@anchorline.local
