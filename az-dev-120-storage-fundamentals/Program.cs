using System.Diagnostics;
using Azure.Identity;
using Azure.Storage.Blobs;
using Microsoft.Extensions.Configuration;

var config = new ConfigurationBuilder()
    .AddEnvironmentVariables("ANCHORLINE_")
    .AddCommandLine(args)
    .Build();

var accountName = config["StorageAccount"] ?? throw new InvalidOperationException("Set ANCHORLINE_StorageAccount");
var containerName = config["Container"] ?? "storefront-images";

var credential = new DefaultAzureCredential();
var primaryUri = new Uri($"https://{accountName}.blob.core.windows.net");
var secondaryUri = new Uri($"https://{accountName}-secondary.blob.core.windows.net");

Console.WriteLine($"Anchorline storage probe → account {accountName}, container {containerName}");
Console.WriteLine();

await Probe(primaryUri, "PRIMARY");
await Probe(secondaryUri, "SECONDARY (RA-* endpoint)");

async Task Probe(Uri endpoint, string label)
{
    Console.WriteLine($"--- {label}: {endpoint} ---");
    var sw = Stopwatch.StartNew();
    try
    {
        var client = new BlobServiceClient(endpoint, credential);
        var container = client.GetBlobContainerClient(containerName);
        await container.CreateIfNotExistsAsync();
        var names = new List<string>();
        await foreach (var blob in container.GetBlobsAsync())
        {
            names.Add(blob.Name);
            if (names.Count >= 10) break;
        }
        sw.Stop();
        Console.WriteLine($"OK — listed {names.Count} blobs in {sw.ElapsedMilliseconds}ms");
        foreach (var n in names) Console.WriteLine($"  · {n}");
    }
    catch (Exception ex)
    {
        sw.Stop();
        Console.WriteLine($"FAIL ({sw.ElapsedMilliseconds}ms) — {ex.GetType().Name}: {ex.Message}");
    }
    Console.WriteLine();
}
