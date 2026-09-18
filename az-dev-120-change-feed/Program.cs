using Azure.Identity;
using Azure.Storage.Blobs;
using Azure.Storage.Blobs.ChangeFeed;

if (args.Length < 2)
{
    Console.Error.WriteLine("Usage: dotnet run -- <account> <command>");
    Console.Error.WriteLine("Commands:");
    Console.Error.WriteLine("  churn <container>     Upload, overwrite, tier, delete a few blobs — generates change feed traffic");
    Console.Error.WriteLine("  replay [hours]        Read change feed for the past N hours (default 1)");
    Environment.Exit(1);
}

var account = args[0];
// Excluding ManagedIdentityCredential: this CLI runs as the student, authenticated
// via `az login` inside the VS Code container — there is no MI to fall back to here,
// and probing for one adds a slow (and in this container, hard-failing) IMDS round trip.
var credential = new DefaultAzureCredential(new DefaultAzureCredentialOptions
{
    ExcludeManagedIdentityCredential = true
});
var serviceUri = new Uri($"https://{account}.blob.core.windows.net");
var blobService = new BlobServiceClient(serviceUri, credential);

switch (args[1])
{
    case "churn":
        await Churn(blobService, args.Length > 2 ? args[2] : "changes");
        break;
    case "replay":
        var hours = args.Length > 2 ? int.Parse(args[2]) : 1;
        await Replay(blobService, hours);
        break;
    default:
        Console.Error.WriteLine($"Unknown command: {args[1]}");
        Environment.Exit(1);
        break;
}

static async Task Churn(BlobServiceClient service, string containerName)
{
    var container = service.GetBlobContainerClient(containerName);
    await container.CreateIfNotExistsAsync();

    Console.WriteLine($"Churning {containerName}...");
    for (var i = 1; i <= 5; i++)
    {
        var blob = container.GetBlobClient($"item-{i}.txt");
        await blob.UploadAsync(BinaryData.FromString($"Anchorline item {i} v1\n"), overwrite: true);
        Console.WriteLine($"  created item-{i}.txt");
    }

    var b2 = container.GetBlobClient("item-2.txt");
    await b2.UploadAsync(BinaryData.FromString("Anchorline item 2 v2 (overwritten)\n"), overwrite: true);
    Console.WriteLine("  overwrote item-2.txt");

    var b3 = container.GetBlobClient("item-3.txt");
    await b3.SetAccessTierAsync(Azure.Storage.Blobs.Models.AccessTier.Cool);
    Console.WriteLine("  tier-changed item-3.txt → Cool");

    var b4 = container.GetBlobClient("item-4.txt");
    await b4.DeleteAsync();
    Console.WriteLine("  deleted item-4.txt");

    Console.WriteLine("Churn done. Change feed batches every ~5 min; wait before replay.");
}

static async Task Replay(BlobServiceClient service, int hours)
{
    var client = service.GetChangeFeedClient();
    var start = DateTimeOffset.UtcNow.AddHours(-hours);
    Console.WriteLine($"Replaying change feed from {start:O} ({hours}h back)...");
    var count = 0;
    await foreach (var change in client.GetChangesAsync(start, DateTimeOffset.UtcNow))
    {
        var typ = change.EventType.ToString();
        var url = change.Subject;
        var etime = change.EventTime.ToString("HH:mm:ss");
        Console.WriteLine($"  {etime}  {typ,-40}  {url}");
        count++;
        if (count >= 50)
        {
            Console.WriteLine("  ... (truncated at 50)");
            break;
        }
    }
    Console.WriteLine($"Replayed {count} events.");
}
