#!/usr/bin/env bash
# Seed some audit blobs into a container for immutability exercises.
# Usage: ./scripts/seed.sh <account> <container> [count]
set -euo pipefail
STG="${1:?Usage: $0 <account> <container> [count]}"
CONT="${2}"
COUNT="${3:-10}"

for i in $(seq 1 "$COUNT"); do
    echo "audit event $i @ $(date -u -Iseconds)" > /tmp/audit-$i.txt
    az storage blob upload --account-name "$STG" --container-name "$CONT" \
        --file /tmp/audit-$i.txt --name "audit-$i.txt" --overwrite \
        --auth-mode login >/dev/null
done
echo "Seeded $COUNT audit blobs."
