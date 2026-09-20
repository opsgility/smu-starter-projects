using Azure.Identity;
using Azure.Messaging.ServiceBus;
using Azure.Storage.Blobs;

var ns = Environment.GetEnvironmentVariable("SB_NAMESPACE") ?? throw new InvalidOperationException("SB_NAMESPACE");
var q = Environment.GetEnvironmentVariable("SB_QUEUE") ?? "claim-check";
var storage = Environment.GetEnvironmentVariable("STORAGE_ACCOUNT") ?? throw new InvalidOperationException("STORAGE_ACCOUNT");
var container = Environment.GetEnvironmentVariable("STORAGE_CONTAINER") ?? "claims";

var cred = new DefaultAzureCredential();
await using var sbClient = new ServiceBusClient(ns, cred);
var blobSvc = new BlobServiceClient(new Uri($"https://{storage}.blob.core.windows.net"), cred);

var mode = args.Length > 0 ? args[0] : "help";
switch (mode)
{
    case "upload": await Upload(int.Parse(args.Length > 1 ? args[1] : "100")); break;
    case "process": await Process(); break;
    default: Console.WriteLine("Modes: upload <sizeMB> | process"); break;
}

async Task Upload(int sizeMB)
{
    var containerClient = blobSvc.GetBlobContainerClient(container);
    await containerClient.CreateIfNotExistsAsync();
    var blobName = $"payload-{Guid.NewGuid():N}.bin";
    var blob = containerClient.GetBlobClient(blobName);
    var payload = new byte[sizeMB * 1024L * 1024L];
    Random.Shared.NextBytes(payload);
    Console.WriteLine($"Uploading {sizeMB} MB blob...");
    var sw = System.Diagnostics.Stopwatch.StartNew();
    using var ms = new MemoryStream(payload);
    await blob.UploadAsync(ms, overwrite: true);
    sw.Stop();
    Console.WriteLine($"Uploaded in {sw.Elapsed}. URL: {blob.Uri}");

    // Send small SB message with the claim-check URL
    await using var sender = sbClient.CreateSender(q);
    await sender.SendMessageAsync(new ServiceBusMessage(blob.Uri.ToString()) { ContentType = "text/x-claim-check" });
    Console.WriteLine("Sent SB claim-check message.");
}

async Task Process()
{
    var processor = sbClient.CreateProcessor(q, new ServiceBusProcessorOptions { MaxConcurrentCalls = 1 });
    processor.ProcessMessageAsync += async args =>
    {
        var url = args.Message.Body.ToString();
        Console.WriteLine($"Claim-check received: {url}");
        var blob = new BlobClient(new Uri(url), cred);
        var sw = System.Diagnostics.Stopwatch.StartNew();
        var resp = await blob.DownloadContentAsync();
        sw.Stop();
        Console.WriteLine($"Downloaded {resp.Value.Content.ToArray().Length / 1024 / 1024} MB in {sw.Elapsed}");
        await args.CompleteMessageAsync(args.Message);
    };
    processor.ProcessErrorAsync += a => { Console.WriteLine($"ERR {a.Exception.Message}"); return Task.CompletedTask; };
    await processor.StartProcessingAsync();
    Console.WriteLine("Processor running. Ctrl-C to stop.");
    await Task.Delay(-1);
}
