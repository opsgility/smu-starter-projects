#!/usr/bin/env bash
# helpers.sh — Lesson 6: Hub-spoke VNets, NSGs, service tags, peering.
#
#     source ./helpers.sh
#
# No side effects at source-time. Every function is opt-in.

set -euo pipefail

require_cli_login() {
    if ! az account show --only-show-errors --query id -o tsv >/dev/null 2>&1; then
        echo "ERROR: not logged in. Run 'az login --use-device-code' first." >&2
        return 1
    fi
}

current_default_group() {
    az config get defaults.group --only-show-errors 2>/dev/null | awk -F'"' '/"value"/ {print $4}'
}

# ---------------------------------------------------------------------------
# VNets + subnets
# ---------------------------------------------------------------------------

# create_hub — create the hub VNet (10.0.0.0/16) with a workload subnet.
create_hub() {
    az network vnet create \
        --name hub-vnet \
        --address-prefix 10.0.0.0/16 \
        --subnet-name workload \
        --subnet-prefix 10.0.1.0/24 \
        --only-show-errors --output table
}

# create_spoke — create the spoke VNet (10.1.0.0/16) with a workload subnet.
create_spoke() {
    az network vnet create \
        --name spoke-vnet \
        --address-prefix 10.1.0.0/16 \
        --subnet-name workload \
        --subnet-prefix 10.1.1.0/24 \
        --only-show-errors --output table
}

# ---------------------------------------------------------------------------
# NSG on the spoke workload subnet
# ---------------------------------------------------------------------------

# create_spoke_nsg — create an NSG + attach it to spoke workload subnet.
# Rules: allow inbound from AzureLoadBalancer service tag; deny inbound Internet.
create_spoke_nsg() {
    az network nsg create --name spoke-nsg --only-show-errors --output table

    az network nsg rule create \
        --nsg-name spoke-nsg \
        --name allow-azurelb \
        --priority 200 \
        --direction Inbound \
        --access Allow \
        --protocol '*' \
        --source-address-prefixes AzureLoadBalancer \
        --destination-port-ranges '*' \
        --only-show-errors --output table

    az network nsg rule create \
        --nsg-name spoke-nsg \
        --name deny-internet \
        --priority 300 \
        --direction Inbound \
        --access Deny \
        --protocol '*' \
        --source-address-prefixes Internet \
        --destination-port-ranges '*' \
        --only-show-errors --output table

    az network vnet subnet update \
        --vnet-name spoke-vnet \
        --name workload \
        --network-security-group spoke-nsg \
        --only-show-errors --output table
}

# ---------------------------------------------------------------------------
# Peering
# ---------------------------------------------------------------------------

# peer_hub_and_spoke — bidirectional peering with forwarded-traffic on both sides.
peer_hub_and_spoke() {
    local sub
    sub="$(az account show --only-show-errors --query id -o tsv)"
    local rg
    rg="$(current_default_group)"

    local hub_id="/subscriptions/${sub}/resourceGroups/${rg}/providers/Microsoft.Network/virtualNetworks/hub-vnet"
    local spoke_id="/subscriptions/${sub}/resourceGroups/${rg}/providers/Microsoft.Network/virtualNetworks/spoke-vnet"

    az network vnet peering create \
        --name hub-to-spoke \
        --vnet-name hub-vnet \
        --remote-vnet "$spoke_id" \
        --allow-vnet-access \
        --allow-forwarded-traffic \
        --only-show-errors --output table

    az network vnet peering create \
        --name spoke-to-hub \
        --vnet-name spoke-vnet \
        --remote-vnet "$hub_id" \
        --allow-vnet-access \
        --allow-forwarded-traffic \
        --only-show-errors --output table
}

# break_peering — delete both peerings so a reachability test proves the failure mode.
break_peering() {
    az network vnet peering delete --name hub-to-spoke   --vnet-name hub-vnet   --only-show-errors
    az network vnet peering delete --name spoke-to-hub   --vnet-name spoke-vnet --only-show-errors
}

# enable_gateway_transit_on_hub — flip allowGatewayTransit on the hub-side peering.
enable_gateway_transit_on_hub() {
    az network vnet peering update \
        --name hub-to-spoke \
        --vnet-name hub-vnet \
        --set allowGatewayTransit=true \
        --only-show-errors --output table
}

# ---------------------------------------------------------------------------
# Ping-based reachability (via run-command, no SSH)
# ---------------------------------------------------------------------------

# ping_between <src-vm> <dest-ip> — ping <dest-ip> from <src-vm> via run-command.
# Returns the run-command output message string; the caller inspects for "0% packet loss"
# or a timeout signature.
ping_between() {
    local src="$1"
    local dest="$2"
    az vm run-command invoke \
        --name "$src" \
        --command-id RunShellScript \
        --scripts "ping -c 3 -W 2 ${dest} || true" \
        --only-show-errors \
        --query "value[0].message" -o tsv
}
