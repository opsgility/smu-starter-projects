using System.Text;
using Azure.Identity;
using Azure.Storage.Blobs;
using Azure.Storage.Blobs.Models;

if (args.Length < 3)
{
    Console.Error.WriteLine("Usage: dotnet run -- <account> <container> <command> [args...]");
    Console.Error.WriteLine("Commands:");
    Console.Error.WriteLine("  upload <blobname> <author> <department> <docType> <year>");
    Console.Error.WriteLine("  seed  <count>                              (uploads N synthetic invoices)");
    Console.Error.WriteLine("  find  <tag-expression>                     e.g., \"documentType = 'invoice' AND year = '2026'\"");
    Console.Error.WriteLine("  list-metadata <blobname>");
    Environment.Exit(1);
}

var account = args[0];
var containerName = args[1];
var command = args[2];

var credential = new DefaultAzureCredential();
var service = new BlobServiceClient(new Uri($"https://{account}.blob.core.windows.net"), credential);
var container = service.GetBlobContainerClient(containerName);
await container.CreateIfNotExistsAsync();

switch (command)
{
    case "upload":
        await Upload(container, args[3], args[4], args[5], args[6], args[7]);
        break;
    case "seed":
        await Seed(container, int.Parse(args[3]));
        break;
    case "find":
        await Find(service, args[3]);
        break;
    case "list-metadata":
        await ListMetadata(container, args[3]);
        break;
    default:
        Console.Error.WriteLine($"Unknown command: {command}");
        Environment.Exit(1);
        break;
}

static async Task Upload(BlobContainerClient container, string name, string author, string department, string documentType, string year)
{
    var blob = container.GetBlobClient(name);
    var content = Encoding.UTF8.GetBytes($"Anchorline document {name}\nAuthor: {author}\nDept: {department}\nType: {documentType}\nYear: {year}\n");
    using var ms = new MemoryStream(content);
    await blob.UploadAsync(ms, new BlobUploadOptions
    {
        Metadata = new Dictionary<string, string>
        {
            ["author"] = author,
            ["department"] = department
        },
        Tags = new Dictionary<string, string>
        {
            ["documentType"] = documentType,
            ["year"] = year
        }
    });
    Console.WriteLine($"Uploaded {name}  metadata=[author={author}, department={department}]  tags=[documentType={documentType}, year={year}]");
}

static async Task Seed(BlobContainerClient container, int count)
{
    var depts = new[] { "sales", "engineering", "finance", "marketing" };
    var types = new[] { "invoice", "report", "contract" };
    var rand = new Random(42);
    for (var i = 1; i <= count; i++)
    {
        var year = (2024 + rand.Next(3)).ToString();
        var dept = depts[rand.Next(depts.Length)];
        var type = types[rand.Next(types.Length)];
        var name = $"{year}/{type}-{i:0000}.txt";
        await Upload(container, name, "seed@anchorline.example", dept, type, year);
    }
    Console.WriteLine($"Seeded {count} blobs.");
}

static async Task Find(BlobServiceClient service, string filter)
{
    Console.WriteLine($"Query: {filter}");
    var count = 0;
    await foreach (var match in service.FindBlobsByTagsAsync(filter))
    {
        Console.WriteLine($"  · {match.BlobContainerName}/{match.BlobName}");
        count++;
        if (count >= 20)
        {
            Console.WriteLine("  ... (truncated at 20)");
            break;
        }
    }
    Console.WriteLine($"Matched {count} (first-page listing).");
}

static async Task ListMetadata(BlobContainerClient container, string name)
{
    var blob = container.GetBlobClient(name);
    var props = await blob.GetPropertiesAsync();
    Console.WriteLine($"Blob: {name}");
    Console.WriteLine("Metadata:");
    foreach (var (k, v) in props.Value.Metadata) Console.WriteLine($"  {k}={v}");
    var tags = await blob.GetTagsAsync();
    Console.WriteLine("Tags:");
    foreach (var (k, v) in tags.Value.Tags) Console.WriteLine($"  {k}={v}");
}
