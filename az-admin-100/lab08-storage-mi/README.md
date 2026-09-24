# lab08-storage-mi — Storage with private access + MI-authenticated blob access

Starter helpers for **Lesson 8** of SMU-CLI-IAAS. Focus: build a passwordless VM-to-storage path — locked-down storage account, VNet rule for one subnet, Entra-based blob upload, user-assigned Managed Identity attached to a VM, and a batch-tag sweep at the end.

## Files

```
lab08-storage-mi/
  README.md              This file.
  helpers.sh             Sourceable bash helpers.
```

## What's in `helpers.sh`

- `create_locked_storage_account <name>` — LRS, Hot, `--allow-blob-public-access false`, `--default-action Deny` (exercise 1).
- `open_vnet_rule <account> <vnet> <subnet>` — turns on `Microsoft.Storage` service endpoint + adds the VNet rule (exercise 2).
- `upload_blob_login <account> <container> <local-file>` — creates the container + uploads a blob using `--auth-mode login` (exercise 3).
- `create_user_mi <name>` — user-assigned Managed Identity (exercise 4).
- `grant_blob_reader_to_mi <mi> <account> <container>` — `Storage Blob Data Reader` at container scope (exercise 4).
- `attach_mi_to_vm <vm> <mi>` — attach the MI to a VM (exercise 5).
- `download_from_vm_via_mi <vm> <account> <container> <blob>` — inside the VM, `az login --identity` then blob download via `--auth-mode login` (exercise 5).
- `tag_all_storage_accounts <tag=value> ...` — batch-tag every storage account in the RG (exercise 6).
- `random_suffix` — 6-char lowercase suffix for globally-unique names like storage accounts.

## How to use

```bash
source ./helpers.sh
az login --use-device-code
require_cli_login
az config set defaults.group=<your-rg> defaults.location=eastus

# Exercise 1
NAME="labstore$(random_suffix)"
create_locked_storage_account "$NAME"

# Exercise 2  — the ARM template pre-provisions vnet + subnet + a VM (`lab08-vm`).
open_vnet_rule "$NAME" lab08-vnet vm-subnet

# Exercise 3
echo "hello from lab 8" > /tmp/sample.txt
upload_blob_login "$NAME" data /tmp/sample.txt

# Exercise 4
create_user_mi lab08-mi
grant_blob_reader_to_mi lab08-mi "$NAME" data

# Exercise 5
attach_mi_to_vm lab08-vm lab08-mi
download_from_vm_via_mi lab08-vm "$NAME" data sample.txt

# Exercise 6
tag_all_storage_accounts env=lab cost-center=cli-course
```

## Notes

- The ARM template attached to this lab pre-provisions `lab08-vnet`, `vm-subnet`, `lab08-nsg`, and `lab08-vm` (Standard_B1s Linux). The helpers assume those names.
- `upload_blob_login` and `download_from_vm_via_mi` deliberately never see a SAS key or connection string — every hop is Entra + RBAC.
- The lab's `LabCredential` grants `Contributor` at RG scope PLUS `Storage Blob Data Reader` scope so `upload_blob_login` succeeds from the student's own identity in exercise 3.
