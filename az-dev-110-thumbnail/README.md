# az-dev-110-thumbnail

Blob-triggered Function that resizes uploaded product images to 300x300 thumbnails.

## Flow

1. Customer uploads to `product-uploads/<name>` (any image format ImageSharp reads).
2. `ThumbnailFunction` fires (blob trigger, default polling — see teaching lesson for Event Grid source).
3. Function resizes to max 300x300 preserving aspect, encodes as JPEG.
4. Output binding writes to `product-thumbnails/<name>.jpg`.

## Concurrency

`host.json` sets `blobs.maxDegreeOfParallelism = 8` — one instance processes 8 images concurrently. Consumption scales out for more.

## Bulk load

`scripts/upload-bulk.sh <storage-account> 100` uploads 100 test images.
