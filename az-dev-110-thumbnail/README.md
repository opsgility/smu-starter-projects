# az-dev-110-thumbnail

Blob-triggered Function that resizes uploaded product images to 300x300 thumbnails.

## Flow

1. Customer uploads to `product-uploads/<name>` (any image format ImageSharp reads).
2. Event Grid delivers `Microsoft.Storage.BlobCreated` to the Function App's blob-extension webhook (Flex Consumption requires Event Grid — polling blob triggers are not supported on FC1).
3. `GenerateThumbnail` fires, resizes to max 300x300 preserving aspect, encodes as JPEG.
4. Output binding writes to `product-thumbnails/<name>.jpg`.

## Bindings + storage connection

The trigger + output use the default `AzureWebJobsStorage` connection. In Azure the ARM template sets `AzureWebJobsStorage__accountName` (identity-based — the Function App's system-assigned managed identity holds `Storage Blob Data Owner` on the account). No connection string is used or needed.

Locally, `local.settings.json` points `AzureWebJobsStorage` at the Storage Emulator (or an Azurite instance).

## Concurrency

`host.json` sets `blobs.maxDegreeOfParallelism = 8` — one instance processes 8 images concurrently. Flex Consumption scales out (per-instance memory + max instance count set in the ARM template) for higher throughput.

## Bulk load

`scripts/upload-bulk.sh <storage-account> 100` uploads 100 test images.
