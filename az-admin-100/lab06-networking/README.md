# lab06-networking — Hub-spoke topology, NSGs, service tags, peering

Starter helpers for **Lesson 6** of SMU-CLI-IAAS. Focus: build a working hub-spoke Azure topology with NSGs and bidirectional peering, prove reachability without opening SSH, then break + re-peer to see the failure mode.

## Files

```
lab06-networking/
  README.md              This file.
  helpers.sh             Sourceable bash helpers.
```

## What's in `helpers.sh`

- `create_hub` — hub VNet 10.0.0.0/16 with a workload subnet 10.0.1.0/24.
- `create_spoke` — spoke VNet 10.1.0.0/16 with a workload subnet 10.1.1.0/24.
- `create_spoke_nsg` — creates the spoke NSG with allow-AzureLoadBalancer + deny-Internet rules and attaches it to the spoke workload subnet.
- `peer_hub_and_spoke` — bidirectional peering with `allow-forwarded-traffic` on both sides.
- `break_peering` — deletes both peerings so the reachability test proves the failure mode (exercise 5).
- `enable_gateway_transit_on_hub` — flips `allowGatewayTransit=true` on the hub-side peering (exercise 6).
- `ping_between <src-vm> <dest-ip>` — runs `ping -c 3` from `<src-vm>` via `az vm run-command invoke`.

## How to use

```bash
source ./helpers.sh
az login --use-device-code
require_cli_login
az config set defaults.group=<your-rg> defaults.location=eastus

# Exercise 1
create_hub
create_spoke

# Exercise 2
create_spoke_nsg

# Exercise 3
peer_hub_and_spoke

# Exercise 4  (deploy one VM per VNet manually first — the lab shows the two az vm create calls)
ping_between hub-vm 10.1.1.4

# Exercise 5
break_peering
ping_between hub-vm 10.1.1.4   # expect timeouts

# Exercise 6
peer_hub_and_spoke
enable_gateway_transit_on_hub
```

## Notes

- The ARM template attached to this lab pre-provisions ONLY the empty resource group — the whole networking stack is student-built.
- `ping_between` uses `|| true` inside the run-command payload so the shell returns success even when packets time out — the calling exercise inspects the returned message string.
- Service tags in NSG rules (`AzureLoadBalancer`, `Internet`, `VirtualNetwork`) are Azure-managed symbolic addresses; the platform keeps their underlying CIDRs current.
