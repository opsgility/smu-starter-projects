#!/usr/bin/env bash
# helpers.sh — Lesson 8: Storage account firewall, MI-authenticated blob access.
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

random_suffix() {
    tr -dc 'a-z0-9' </dev/urandom | head -c 6
}

# ---------------------------------------------------------------------------
# Storage account with private access
# ---------------------------------------------------------------------------

# create_locked_storage_account <name> — LRS, Hot tier, no public blob access, deny by default.
create_locked_storage_account() {
    local name="$1"
    az storage account create \
        --name "$name" \
        --sku Standard_LRS \
        --access-tier Hot \
        --allow-blob-public-access false \
        --default-action Deny \
        --only-show-errors \
        --output table
}

# open_vnet_rule <account> <vnet> <subnet> — allow one subnet to reach the storage account.
open_vnet_rule() {
    local account="$1"
    local vnet="$2"
    local subnet="$3"

    # Turn on the Microsoft.Storage service endpoint on the subnet first — idempotent.
    az network vnet subnet update \
        --vnet-name "$vnet" \
        --name "$subnet" \
        --service-endpoints Microsoft.Storage \
        --only-show-errors --output none

    az storage account network-rule add \
        --account-name "$account" \
        --vnet-name "$vnet" \
        --subnet "$subnet" \
        --only-show-errors --output table
}

# ---------------------------------------------------------------------------
# Blob upload / download with --auth-mode login
# ---------------------------------------------------------------------------

# upload_blob_login <account> <container> <local-file> [<blob-name>] — upload via Entra identity.
upload_blob_login() {
    local account="$1"
    local container="$2"
    local file="$3"
    local blob="${4:-$(basename "$file")}"

    az storage container create \
        --account-name "$account" \
        --name "$container" \
        --auth-mode login \
        --only-show-errors --output none

    az storage blob upload \
        --account-name "$account" \
        --container-name "$container" \
        --file "$file" \
        --name "$blob" \
        --auth-mode login \
        --overwrite \
        --only-show-errors --output table
}

# ---------------------------------------------------------------------------
# User-assigned managed identity
# ---------------------------------------------------------------------------

# create_user_mi <name> — create a user-assigned MI in the default RG.
create_user_mi() {
    local name="$1"
    az identity create \
        --name "$name" \
        --only-show-errors \
        --output table
}

# grant_blob_reader_to_mi <mi-name> <account> <container> — assign
# Storage Blob Data Reader at container scope to the MI.
grant_blob_reader_to_mi() {
    local mi="$1"
    local account="$2"
    local container="$3"
    local rg
    rg="$(current_default_group)"
    local sub
    sub="$(az account show --only-show-errors --query id -o tsv)"

    local mi_pid
    mi_pid="$(az identity show -g "$rg" -n "$mi" --only-show-errors --query principalId -o tsv)"

    local scope="/subscriptions/${sub}/resourceGroups/${rg}/providers/Microsoft.Storage/storageAccounts/${account}/blobServices/default/containers/${container}"

    az role assignment create \
        --assignee-object-id "$mi_pid" \
        --assignee-principal-type ServicePrincipal \
        --role "Storage Blob Data Reader" \
        --scope "$scope" \
        --only-show-errors \
        --output table
}

# attach_mi_to_vm <vm-name> <mi-name> — attach a user-assigned MI to a VM.
attach_mi_to_vm() {
    local vm="$1"
    local mi="$2"
    local rg
    rg="$(current_default_group)"

    local mi_id
    mi_id="$(az identity show -g "$rg" -n "$mi" --only-show-errors --query id -o tsv)"

    az vm identity assign \
        --name "$vm" \
        --identities "$mi_id" \
        --only-show-errors \
        --output table
}

# download_from_vm_via_mi <vm-name> <account> <container> <blob> — inside the VM,
# `az login --identity` then `az storage blob download --auth-mode login`.
download_from_vm_via_mi() {
    local vm="$1"
    local account="$2"
    local container="$3"
    local blob="$4"

    az vm run-command invoke \
        --name "$vm" \
        --command-id RunShellScript \
        --scripts "az login --identity --only-show-errors && az storage blob download --account-name ${account} --container-name ${container} --name ${blob} --file /tmp/${blob} --auth-mode login --only-show-errors && ls -l /tmp/${blob}" \
        --only-show-errors \
        --query "value[0].message" -o tsv
}

# ---------------------------------------------------------------------------
# Batch tagging
# ---------------------------------------------------------------------------

# tag_all_storage_accounts <tag=value> [<tag=value>...] — apply tags to every storage
# account in the default RG in one sweep.
tag_all_storage_accounts() {
    local rg
    rg="$(current_default_group)"
    local id
    while IFS= read -r id; do
        az resource tag \
            --ids "$id" \
            --tags "$@" \
            --only-show-errors \
            --output none
        echo "tagged ${id##*/}"
    done < <(az storage account list --resource-group "$rg" --only-show-errors --query "[].id" -o tsv)
}
