using Azure.Messaging;
using Microsoft.Azure.Cosmos;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.Logging;

namespace Anchorline.Functions.EventGridCosmos;

public class HandleBlobCreated
{
    private readonly ILogger<HandleBlobCreated> _log;
    private readonly Container _container;

    public HandleBlobCreated(ILogger<HandleBlobCreated> log, CosmosClient cosmos)
    {
        _log = log;

        var dbName = Environment.GetEnvironmentVariable("COSMOS_DATABASE") ?? "Anchorline";
        var containerName = Environment.GetEnvironmentVariable("COSMOS_CONTAINER") ?? "ProductUploads";
        _container = cosmos.GetContainer(dbName, containerName);
    }

    public class ProductUploadRecord
    {
        public required string id { get; set; }
        public required string BlobUrl { get; set; }
        public required string EventType { get; set; }
        public required string EventTime { get; set; }
        public required string Source { get; set; }
        public required string Subject { get; set; }
        public required string EventId { get; set; }
    }

    [Function("HandleBlobCreated")]
    public async Task Run([EventGridTrigger] CloudEvent evt)
    {
        _log.LogInformation("CloudEvent id={Id} type={Type} subject={Subject}",
            evt.Id, evt.Type, evt.Subject);

        if (evt.Type != "Microsoft.Storage.BlobCreated")
        {
            _log.LogInformation("Ignoring non-blob-created event type={Type}", evt.Type);
            return;
        }

        var data = evt.Data?.ToObjectFromJson<System.Text.Json.JsonElement>();
        var url = data.HasValue && data.Value.TryGetProperty("url", out var u)
            ? u.GetString() ?? ""
            : "";

        // Idempotency: key on the blob's stable business identity (the file name inside the
        // container), not evt.Id. evt.Id changes on every upload — so blob-overwrite retries
        // would produce duplicate documents. The subject looks like:
        //   /blobServices/default/containers/product-uploads/blobs/scan-001.json
        // We take the segment after "/blobs/" as the doc id. Upsert with a stable id means:
        //   - Event Grid retry (same event id, same subject) -> upsert overwrites -> ONE doc.
        //   - Blob re-upload (new event id, same subject)     -> upsert overwrites -> ONE doc.
        var subject = evt.Subject ?? "";
        var idx = subject.LastIndexOf("/blobs/", StringComparison.OrdinalIgnoreCase);
        var docId = (idx >= 0 ? subject[(idx + "/blobs/".Length)..] : subject).Replace('/', '-');
        if (string.IsNullOrWhiteSpace(docId)) docId = evt.Id;

        var record = new ProductUploadRecord
        {
            id = docId,
            BlobUrl = url,
            EventType = evt.Type,
            EventTime = evt.Time?.ToString("o") ?? "",
            Source = evt.Source?.ToString() ?? "",
            Subject = subject,
            EventId = evt.Id
        };

        _log.LogInformation("Upserting Cosmos doc id={DocId} url={Url} eventId={EventId}",
            docId, url, evt.Id);

        await _container.UpsertItemAsync(record, new PartitionKey(docId));

        // Emit the current document count as a trace so students can verify idempotency
        // end-to-end from Application Insights without a data-plane query tool.
        var countIter = _container.GetItemQueryIterator<int>(
            new QueryDefinition("SELECT VALUE COUNT(1) FROM c"));
        var total = 0;
        while (countIter.HasMoreResults)
        {
            foreach (var n in await countIter.ReadNextAsync()) total += n;
        }
        _log.LogInformation("Cosmos ProductUploads count after upsert: {Count} (docId={DocId})",
            total, docId);
    }
}
