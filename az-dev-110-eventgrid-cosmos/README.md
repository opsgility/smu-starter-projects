# az-dev-110-eventgrid-cosmos

Anchorline's Event Grid → Function → Cosmos pipeline. Every `Microsoft.Storage.BlobCreated` event
on the `product-uploads` container becomes a document in the `Anchorline` database, `ProductUploads`
container.

## Idempotency

The Cosmos document id is derived from the CloudEvent `subject` (the blob's stable business
identity — the file name inside the container), not from `evt.Id`. Combined with an `UpsertItem`
call, this keeps the document count at ONE per blob regardless of:

- Event Grid retrying the same event (at-least-once delivery)
- The student re-uploading the same blob name (overwrite fires a new event with a new `evt.Id`)

## Runtime contract (from the lab ARM template)

| App setting | Purpose |
|-------------|---------|
| `COSMOS_ENDPOINT` | Cosmos account endpoint URL, consumed via `DefaultAzureCredential` in `Program.cs`. |
| `COSMOS_DATABASE` | `Anchorline` |
| `COSMOS_CONTAINER` | `ProductUploads` |
| `UPLOADS_CONTAINER` | `product-uploads` (source blob container) |
| `AzureWebJobsStorage__accountName` | Identity-based storage for the Functions host. |

The Function App's system-assigned managed identity is pre-granted `Cosmos DB Built-in Data
Contributor` (`00000000-0000-0000-0000-000000000002`) on the account by the ARM template.
