// =============================================================================
//  SECURE SECRETS MANAGEMENT — Security Challenge
// =============================================================================
//  6 secrets management vulnerabilities in AppConfig.cs and DatabaseClient.cs.
//  Run: dotnet run
// =============================================================================

using Microsoft.Extensions.Configuration;

// Simulate production environment variables
Environment.SetEnvironmentVariable("DB_CONNECTION_STRING", "Server=test-db;Database=testapp;User=testuser;Password=TestPass!;");
Environment.SetEnvironmentVariable("API_KEY", "sk-test-fromenv-xyz789");
Environment.SetEnvironmentVariable("SMTP_PASSWORD", "test-smtp-secret");

var appConfig = new AppConfig();
var dbClient = new DatabaseClient();

Console.WriteLine("╔══════════════════════════════════════════════════════════╗");
Console.WriteLine("║      SECURE SECRETS MANAGEMENT — Security Challenge     ║");
Console.WriteLine("║      Find and fix all 6 vulnerabilities!                ║");
Console.WriteLine("╚══════════════════════════════════════════════════════════╝");
Console.WriteLine();

int passed = 0;
int failed = 0;

void RunCheck(string name, Func<bool> check)
{
    try
    {
        bool result = check();
        if (result) { Console.ForegroundColor = ConsoleColor.Green; Console.WriteLine($"  ✓ PASS  {name}"); passed++; }
        else { Console.ForegroundColor = ConsoleColor.Red; Console.WriteLine($"  ✗ FAIL  {name}"); failed++; }
    }
    catch (Exception ex) { Console.ForegroundColor = ConsoleColor.Red; Console.WriteLine($"  ✗ CRASH {name}"); Console.ForegroundColor = ConsoleColor.DarkRed; Console.WriteLine($"          {ex.GetType().Name}: {ex.Message}"); failed++; }
    Console.ResetColor();
}

Console.WriteLine("─── Hardcoded Secrets ───");
RunCheck("Connection string is NOT hardcoded (reads from env)", () =>
{
    string connStr = dbClient.GetConnectionString();
    return !connStr.Contains("P@ssw0rd123"); // Should not contain the hardcoded password
});

RunCheck("API key is NOT hardcoded (reads from env)", () =>
{
    string key = appConfig.GetApiKey();
    return key != "sk-live-abc123def456"; // Should not be the hardcoded value
});

RunCheck("SMTP password NOT in appsettings.json (reads from env)", () =>
{
    var config = new ConfigurationBuilder()
        .AddJsonFile("appsettings.json", optional: true)
        .AddEnvironmentVariables()
        .Build();
    string smtpPass = config["SmtpPassword"] ?? "";
    return smtpPass != "realpassword123"; // Should come from env, not JSON
});

Console.WriteLine("─── Secret Leakage ───");
RunCheck("Connect() does NOT log the connection string", () =>
{
    var client = new DatabaseClient();
    client.Connect();
    // Check log output doesn't contain passwords
    return client.LogOutput.All(log => !log.Contains("Password=") && !log.Contains("P@ssw0rd"));
});

RunCheck("GetApiHeaders() does NOT write to Debug output", () =>
{
    // Capture debug output
    var debugListener = new System.Diagnostics.TextWriterTraceListener(new System.IO.StringWriter());
    System.Diagnostics.Debug.Listeners.Add(debugListener);
    appConfig.GetApiHeaders();
    debugListener.Flush();
    string debugOutput = ((System.IO.StringWriter)debugListener.Writer!).ToString();
    System.Diagnostics.Debug.Listeners.Remove(debugListener);
    return !debugOutput.Contains("sk-live") && !debugOutput.Contains("Using key:");
});

Console.WriteLine("─── Encryption vs Encoding ───");
RunCheck("Config 'encryption' is NOT just Base64 encoding", () =>
{
    string original = "MySuperSecretValue";
    string base64 = Convert.ToBase64String(System.Text.Encoding.UTF8.GetBytes(original));
    // If LoadEncryptedConfig just does Base64 decode, it will return the original
    // Real encryption would not decode to original via simple Base64
    return appConfig.IsRealEncryption(original, base64) == false
        ? false   // Still just Base64
        : true;   // Real encryption or at least not trivially decodable

    // Simpler test: encode something, "decrypt" it — should NOT return original if properly encrypted
});

Console.WriteLine();
Console.WriteLine("══════════════════════════════════════════════════════════");
if (failed == 0) { Console.ForegroundColor = ConsoleColor.Green; Console.WriteLine($"  ALL {passed} CHECKS PASSED — Secrets are secure! 🔒"); }
else { Console.ForegroundColor = ConsoleColor.Yellow; Console.WriteLine($"  {passed} passed, {failed} failed — {failed} vulnerability(ies) remaining."); Console.WriteLine("  Fix the vulnerabilities and run again: dotnet run"); }
Console.ResetColor();
Console.WriteLine("══════════════════════════════════════════════════════════");
Console.WriteLine();
