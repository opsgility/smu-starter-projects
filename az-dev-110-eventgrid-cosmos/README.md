# az-dev-110-eventgrid-cosmos

Anchorline's Event Grid → Function → Cosmos pipeline. Every blob-created event on `product-uploads` becomes a Cosmos document. Uses `evt.Id` as the Cosmos document id — idempotent on duplicate delivery.
