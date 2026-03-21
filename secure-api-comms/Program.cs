// =============================================================================
//  SECURE API COMMUNICATION — Security Challenge
// =============================================================================
//  6 API security vulnerabilities in ApiClient.cs and DataParser.cs.
//  Run: dotnet run
// =============================================================================

using System.Text.Json;

var client = new ApiClient();
var parser = new DataParser();

Console.WriteLine("╔══════════════════════════════════════════════════════════╗");
Console.WriteLine("║      SECURE API COMMUNICATION — Security Challenge      ║");
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

Console.WriteLine("─── Transport Security ───");
RunCheck("SSL certificate validation is NOT disabled", () =>
{
    return !client.HasCertificateValidationDisabled();
});

RunCheck("Data URL uses HTTPS, not HTTP", () =>
{
    string url = client.GetDataUrl();
    return url.StartsWith("https://");
});

Console.WriteLine("─── Credential Security ───");
RunCheck("Authentication credentials are in headers, not URL", () =>
{
    var (url, headers) = client.Authenticate("sk-test-key", "sk-test-secret");
    bool urlClean = !url.Contains("sk-test-key") && !url.Contains("sk-test-secret");
    bool headersHaveAuth = headers.ContainsKey("Authorization") || headers.ContainsKey("X-Api-Key");
    return urlClean && headersHaveAuth;
});

RunCheck("Search URL properly encodes user input", () =>
{
    string url = client.BuildSearchUrl("test query&evil=true");
    // Properly encoded: spaces become %20, & becomes %26
    return url.Contains("test%20query%26evil%3Dtrue") || url.Contains("test+query");
});

Console.WriteLine("─── Client Configuration ───");
RunCheck("HttpClient has a reasonable timeout (< 60s)", () =>
{
    var timeout = client.GetTimeout();
    return timeout.TotalSeconds > 0 && timeout.TotalSeconds <= 60;
});

RunCheck("JSON deserialization rejects deeply nested input", () =>
{
    // Build a deeply nested JSON string (100 levels)
    string deepJson = "";
    for (int i = 0; i < 100; i++) deepJson += "{\"a\":";
    deepJson += "1";
    for (int i = 0; i < 100; i++) deepJson += "}";

    bool blocked = false;
    try
    {
        parser.ParseResponse<JsonElement>(deepJson);
    }
    catch (JsonException) { blocked = true; }
    catch (ArgumentException) { blocked = true; }
    return blocked;
});

Console.WriteLine();
Console.WriteLine("══════════════════════════════════════════════════════════");
if (failed == 0) { Console.ForegroundColor = ConsoleColor.Green; Console.WriteLine($"  ALL {passed} CHECKS PASSED — API communication is secure! 🔒"); }
else { Console.ForegroundColor = ConsoleColor.Yellow; Console.WriteLine($"  {passed} passed, {failed} failed — {failed} vulnerability(ies) remaining."); Console.WriteLine("  Fix the vulnerabilities and run again: dotnet run"); }
Console.ResetColor();
Console.WriteLine("══════════════════════════════════════════════════════════");
Console.WriteLine();
