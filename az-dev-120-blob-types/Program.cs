using System.Diagnostics;
using System.Text;
using Azure.Identity;
using Azure.Storage;
using Azure.Storage.Blobs;
using Azure.Storage.Blobs.Models;
using Azure.Storage.Blobs.Specialized;

if (args.Length < 3)
{
    Console.Error.WriteLine("Usage: dotnet run -- <account> <container> <command> [args...]");
    Console.Error.WriteLine("Commands:");
    Console.Error.WriteLine("  upload-single <file> <blobname>       Upload with default single-connection settings");
    Console.Error.WriteLine("  upload-parallel <file> <blobname>     Upload with 8 parallel × 8 MiB blocks");
    Console.Error.WriteLine("  append-log <blobname> <lines>         Append N text lines to an append blob");
    Environment.Exit(1);
}

var account = args[0];
var container = args[1];
var command = args[2];

var credential = new DefaultAzureCredential();
var serviceClient = new BlobServiceClient(
    new Uri($"https://{account}.blob.core.windows.net"), credential);
var containerClient = serviceClient.GetBlobContainerClient(container);
await containerClient.CreateIfNotExistsAsync();

switch (command)
{
    case "upload-single":
        await UploadFile(containerClient, args[3], args[4], parallel: false);
        break;
    case "upload-parallel":
        await UploadFile(containerClient, args[3], args[4], parallel: true);
        break;
    case "append-log":
        await AppendLog(containerClient, args[3], int.Parse(args[4]));
        break;
    default:
        Console.Error.WriteLine($"Unknown command: {command}");
        Environment.Exit(1);
        break;
}

static async Task UploadFile(BlobContainerClient container, string filePath, string blobName, bool parallel)
{
    var fileInfo = new FileInfo(filePath);
    if (!fileInfo.Exists)
    {
        Console.Error.WriteLine($"File not found: {filePath}");
        Environment.Exit(1);
    }

    Console.WriteLine($"Uploading {fileInfo.Length / 1024.0 / 1024.0:F1} MiB → {blobName}");
    Console.WriteLine($"Mode: {(parallel ? "PARALLEL (8 × 8 MiB blocks)" : "SINGLE-CONNECTION default")}");

    var blob = container.GetBlobClient(blobName);
    var options = new BlobUploadOptions
    {
        TransferOptions = parallel
            ? new StorageTransferOptions
                {
                    InitialTransferSize = 8 * 1024 * 1024,
                    MaximumTransferSize = 8 * 1024 * 1024,
                    MaximumConcurrency = 8
                }
            : new StorageTransferOptions
                {
                    InitialTransferSize = long.MaxValue,
                    MaximumConcurrency = 1
                }
    };

    var sw = Stopwatch.StartNew();
    await using var stream = File.OpenRead(filePath);
    await blob.UploadAsync(stream, options);
    sw.Stop();

    var mbps = (fileInfo.Length * 8.0) / (sw.Elapsed.TotalSeconds * 1024 * 1024);
    Console.WriteLine($"Done in {sw.Elapsed.TotalSeconds:F1}s — {mbps:F1} Mbps");
}

static async Task AppendLog(BlobContainerClient container, string blobName, int lines)
{
    var appendBlob = container.GetAppendBlobClient(blobName);
    await appendBlob.CreateIfNotExistsAsync();

    var sw = Stopwatch.StartNew();
    for (var i = 1; i <= lines; i++)
    {
        var line = $"{DateTimeOffset.UtcNow:o} anchorline event #{i}\n";
        var bytes = Encoding.UTF8.GetBytes(line);
        using var ms = new MemoryStream(bytes);
        await appendBlob.AppendBlockAsync(ms);
    }
    sw.Stop();
    var props = await appendBlob.GetPropertiesAsync();
    Console.WriteLine($"Appended {lines} lines in {sw.Elapsed.TotalSeconds:F1}s");
    Console.WriteLine($"Blob size: {props.Value.ContentLength} bytes");
}
