#!/usr/bin/env bash
# Try to delete a blob and report the outcome.
# Usage: ./scripts/try-delete.sh <account> <container> <blob-name>
set -euo pipefail
STG="${1:?Usage: $0 <account> <container> <blob-name>}"
CONT="${2}"
NAME="${3}"

echo "Attempting to delete $CONT/$NAME..."
if az storage blob delete --account-name "$STG" --container-name "$CONT" --name "$NAME" --auth-mode login 2>/tmp/delete.err; then
    echo "  Deleted successfully. (blob is NOT immutable — check policy state)"
else
    echo "  Delete FAILED — blob is protected."
    cat /tmp/delete.err
fi
