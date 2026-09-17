#!/usr/bin/env bash
# Bulk upload sample images to product-uploads for a load test.
# Usage: ./scripts/upload-bulk.sh <storage-account-name> <count>

set -euo pipefail
STG="${1:?Usage: $0 <storage-account> [count]}"
COUNT="${2:-50}"

echo "Generating $COUNT sample images..."
mkdir -p /tmp/anchorline-images
for i in $(seq 1 "$COUNT"); do
    # 800x600 random-colored JPG via ImageMagick if present, else a copy of one seed image
    if command -v convert &> /dev/null; then
        convert -size 800x600 "xc:hsl($((i * 7 % 360)),80%,60%)" "/tmp/anchorline-images/img-$i.jpg"
    else
        # fallback: reuse one image
        [ -f /tmp/anchorline-images/img-0.jpg ] || dd if=/dev/urandom of=/tmp/anchorline-images/img-0.jpg bs=1024 count=50 2>/dev/null
        cp /tmp/anchorline-images/img-0.jpg "/tmp/anchorline-images/img-$i.jpg"
    fi
done

echo "Uploading to $STG/product-uploads..."
az storage blob upload-batch \
    --account-name "$STG" \
    --destination product-uploads \
    --source /tmp/anchorline-images \
    --pattern "img-*.jpg" \
    --overwrite \
    --auth-mode login

echo "Done. $COUNT images uploaded."
