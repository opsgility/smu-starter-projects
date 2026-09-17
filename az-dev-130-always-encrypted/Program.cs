using Azure.Core;
using Azure.Identity;
using Microsoft.Data.SqlClient;
using Microsoft.Data.SqlClient.AlwaysEncrypted.AzureKeyVaultProvider;

var server = Environment.GetEnvironmentVariable("ANCHORLINE_SQL_SERVER")
    ?? throw new InvalidOperationException("ANCHORLINE_SQL_SERVER not set");
var database = Environment.GetEnvironmentVariable("ANCHORLINE_SQL_DATABASE") ?? "AnchorlineOrders";

var cred = new DefaultAzureCredential();

// Register the Key Vault provider so Always Encrypted can unwrap CEKs at runtime.
var akvProvider = new SqlColumnEncryptionAzureKeyVaultProvider(cred);
SqlConnection.RegisterColumnEncryptionKeyStoreProviders(
    new Dictionary<string, SqlColumnEncryptionKeyStoreProvider>(StringComparer.OrdinalIgnoreCase)
    {
        [SqlColumnEncryptionAzureKeyVaultProvider.ProviderName] = akvProvider
    });

var token = await cred.GetTokenAsync(new TokenRequestContext(new[] { "https://database.windows.net/.default" }));

var mode = args.Length > 0 ? args[0] : "help";
switch (mode)
{
    case "seed":  await Seed(); break;
    case "read-ae":  await Read(withAe: true); break;
    case "read-plain": await Read(withAe: false); break;
    case "find-email": await FindByEmail(args.Length > 1 ? args[1] : "alice@example.com"); break;
    default: Console.WriteLine("Modes: seed | read-ae | read-plain | find-email <email>"); break;
}

async Task Seed()
{
    // Insertion path uses AE-enabled connection so parameters go in as ciphertext.
    await using var conn = OpenAe();
    await using var cmd = conn.CreateCommand();
    cmd.CommandText = "INSERT INTO dbo.Customer(Name, Email, Ssn) VALUES(@n, @e, @s)";
    cmd.Parameters.Add(new SqlParameter("@n", "Alice Waters"));
    cmd.Parameters.Add(new SqlParameter("@e", "alice@example.com"));
    cmd.Parameters.Add(new SqlParameter("@s", "123-45-6789"));
    await cmd.ExecuteNonQueryAsync();

    cmd.Parameters["@n"].Value = "Bob Rivers";
    cmd.Parameters["@e"].Value = "bob@example.com";
    cmd.Parameters["@s"].Value = "987-65-4321";
    await cmd.ExecuteNonQueryAsync();

    Console.WriteLine("Seeded 2 customers with encrypted PII.");
}

async Task Read(bool withAe)
{
    await using var conn = withAe ? OpenAe() : OpenPlain();
    await using var cmd = conn.CreateCommand();
    cmd.CommandText = "SELECT TOP 5 CustomerId, Name, Email, Ssn FROM dbo.Customer";
    await using var r = await cmd.ExecuteReaderAsync();
    Console.WriteLine("Id | Name              | Email                    | Ssn");
    while (await r.ReadAsync())
    {
        // With AE off, Email/Ssn come back as byte[] (ciphertext). Render as hex prefix.
        var email = r["Email"] switch
        {
            byte[] b => "0x" + BitConverter.ToString(b, 0, Math.Min(16, b.Length)).Replace("-", "") + "...",
            var x => x.ToString()
        };
        var ssn = r["Ssn"] switch
        {
            byte[] b => "0x" + BitConverter.ToString(b, 0, Math.Min(16, b.Length)).Replace("-", "") + "...",
            var x => x.ToString()
        };
        Console.WriteLine($"{r["CustomerId"]} | {r["Name"],-16} | {email,-24} | {ssn}");
    }
}

async Task FindByEmail(string email)
{
    // Deterministic AE lets a WHERE Email = @e work — the parameter is encrypted client-side to
    // the same ciphertext, and the DB matches on ciphertext bytes.
    await using var conn = OpenAe();
    await using var cmd = conn.CreateCommand();
    cmd.CommandText = "SELECT CustomerId, Name, Email, Ssn FROM dbo.Customer WHERE Email = @e";
    var p = cmd.Parameters.Add(new SqlParameter("@e", System.Data.SqlDbType.NVarChar, 200));
    p.Value = email;
    await using var r = await cmd.ExecuteReaderAsync();
    if (!await r.ReadAsync()) { Console.WriteLine($"No match for {email}"); return; }
    Console.WriteLine($"Found: {r["CustomerId"]} | {r["Name"]} | {r["Email"]} | {r["Ssn"]}");
}

SqlConnection OpenAe()
{
    var cs = $"Server=tcp:{server},1433;Database={database};Encrypt=True;Connection Timeout=30;Column Encryption Setting=Enabled;";
    var c = new SqlConnection(cs) { AccessToken = token.Token };
    c.Open();
    return c;
}
SqlConnection OpenPlain()
{
    var cs = $"Server=tcp:{server},1433;Database={database};Encrypt=True;Connection Timeout=30;";
    var c = new SqlConnection(cs) { AccessToken = token.Token };
    c.Open();
    return c;
}
