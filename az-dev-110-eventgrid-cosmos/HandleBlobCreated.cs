using Azure.Messaging;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.Logging;

namespace Anchorline.Functions.EventGridCosmos;

public class HandleBlobCreated
{
    private readonly ILogger<HandleBlobCreated> _log;

    public HandleBlobCreated(ILogger<HandleBlobCreated> log) => _log = log;

    public class ProductUploadRecord
    {
        public required string id { get; set; }
        public required string BlobUrl { get; set; }
        public required string EventType { get; set; }
        public required string EventTime { get; set; }
        public required string Source { get; set; }
    }

    [Function("HandleBlobCreated")]
    [CosmosDBOutput(
        databaseName: "Anchorline",
        containerName: "ProductUploads",
        Connection = "CosmosConnection",
        CreateIfNotExists = false)]
    public ProductUploadRecord? Run([EventGridTrigger] CloudEvent evt)
    {
        _log.LogInformation("CloudEvent id={Id} type={Type} source={Source}", evt.Id, evt.Type, evt.Source);

        if (evt.Type != "Microsoft.Storage.BlobCreated")
        {
            _log.LogInformation("Ignoring non-blob-created event");
            return null;
        }

        var data = evt.Data?.ToObjectFromJson<System.Text.Json.JsonElement>();
        var url = data?.GetProperty("url").GetString() ?? "";

        return new ProductUploadRecord
        {
            id = evt.Id,               // <- eventId as the Cosmos doc id = idempotency
            BlobUrl = url,
            EventType = evt.Type,
            EventTime = evt.Time?.ToString("o") ?? "",
            Source = evt.Source ?? ""
        };
    }
}
