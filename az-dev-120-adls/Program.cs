using Azure.Identity;
using Azure.Storage.Files.DataLake;
using Azure.Storage.Files.DataLake.Models;

if (args.Length < 3)
{
    Console.Error.WriteLine("Usage: dotnet run -- <account> <filesystem> <command> [args...]");
    Console.Error.WriteLine("Commands:");
    Console.Error.WriteLine("  scaffold                             Create tenants/{acme,contoso}/data/<date>/ tree + a sample file each");
    Console.Error.WriteLine("  show-acl <path>                      Show POSIX ACL on a directory or file");
    Console.Error.WriteLine("  set-acl  <path> <acl-string>         Set POSIX ACL (e.g., \"user::rwx,group::r-x,other::---\")");
    Console.Error.WriteLine("  rename <from-path> <to-path>         Atomic directory rename");
    Console.Error.WriteLine("  list-recursive <path>                Recursive listing under a directory");
    Environment.Exit(1);
}

var account = args[0];
var fsName = args[1];
var command = args[2];

var credential = new DefaultAzureCredential();
var svc = new DataLakeServiceClient(new Uri($"https://{account}.dfs.core.windows.net"), credential);
var fs = svc.GetFileSystemClient(fsName);
await fs.CreateIfNotExistsAsync();

switch (command)
{
    case "scaffold":
        await Scaffold(fs);
        break;
    case "show-acl":
        await ShowAcl(fs, args[3]);
        break;
    case "set-acl":
        await SetAcl(fs, args[3], args[4]);
        break;
    case "rename":
        await Rename(fs, args[3], args[4]);
        break;
    case "list-recursive":
        await ListRecursive(fs, args[3]);
        break;
    default:
        Console.Error.WriteLine($"Unknown command: {command}");
        Environment.Exit(1);
        break;
}

static async Task Scaffold(DataLakeFileSystemClient fs)
{
    var today = DateTimeOffset.UtcNow.ToString("yyyy-MM-dd");
    foreach (var tenant in new[] { "acme", "contoso" })
    {
        var dir = fs.GetDirectoryClient($"tenants/{tenant}/data/{today}");
        await dir.CreateIfNotExistsAsync();
        var file = dir.GetFileClient("sample.json");
        var body = $"{{\"tenant\":\"{tenant}\",\"date\":\"{today}\"}}";
        await file.UploadAsync(BinaryData.FromString(body).ToStream(), overwrite: true);
        Console.WriteLine($"  created tenants/{tenant}/data/{today}/sample.json");
    }
}

static async Task ShowAcl(DataLakeFileSystemClient fs, string path)
{
    var pathClient = fs.GetDirectoryClient(path);
    var props = await pathClient.GetAccessControlAsync();
    Console.WriteLine($"Path: {path}");
    Console.WriteLine($"  Owner: {props.Value.Owner}");
    Console.WriteLine($"  Group: {props.Value.Group}");
    Console.WriteLine($"  Permissions: {props.Value.Permissions}");
    Console.WriteLine("  ACL entries:");
    foreach (var entry in props.Value.AccessControlList)
    {
        Console.WriteLine($"    {entry.AccessControlType}::{entry.EntityId ?? "-"} {entry.Permissions} default={entry.DefaultScope}");
    }
}

static async Task SetAcl(DataLakeFileSystemClient fs, string path, string aclString)
{
    var pathClient = fs.GetDirectoryClient(path);
    var acl = PathAccessControlExtensions.ParseAccessControlList(aclString);
    await pathClient.SetAccessControlListAsync(acl);
    Console.WriteLine($"Set ACL on {path}: {aclString}");
}

static async Task Rename(DataLakeFileSystemClient fs, string from, string to)
{
    var src = fs.GetDirectoryClient(from);
    var start = DateTimeOffset.UtcNow;
    var result = await src.RenameAsync(destinationPath: to);
    var elapsed = DateTimeOffset.UtcNow - start;
    Console.WriteLine($"Renamed {from} → {to} in {elapsed.TotalMilliseconds:F0}ms (atomic).");
}

static async Task ListRecursive(DataLakeFileSystemClient fs, string path)
{
    Console.WriteLine($"Recursive listing under {path}:");
    await foreach (var item in fs.GetPathsAsync(path: path, recursive: true, userPrincipalName: false))
    {
        var kind = item.IsDirectory == true ? "DIR " : "FILE";
        Console.WriteLine($"  {kind}  {item.Name}");
    }
}
