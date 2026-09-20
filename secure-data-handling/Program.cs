// =============================================================================
//  SECURE DATA HANDLING — Security Challenge
// =============================================================================
//  6 data exposure vulnerabilities in CustomerService.cs.
//  Run: dotnet run
//  Fix all 6 to make every check PASS.
// =============================================================================

var service = new CustomerService();

Console.WriteLine("╔══════════════════════════════════════════════════════════╗");
Console.WriteLine("║       SECURE DATA HANDLING — Security Challenge         ║");
Console.WriteLine("║       Find and fix all 6 vulnerabilities!               ║");
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

// ── Check 1: Exception messages ───────────────────────────────────────
Console.WriteLine("─── Data in Exceptions ───");
RunCheck("Exception does NOT contain full card number or CVV", () =>
{
    try
    {
        service.ProcessPayment("4111222233334444", "123", -1);
        return false; // Should have thrown
    }
    catch (Exception ex)
    {
        bool hasFullCard = ex.Message.Contains("4111222233334444");
        bool hasCvv = ex.Message.Contains("123");
        bool hasLast4 = ex.Message.Contains("4444"); // Last 4 is OK
        return !hasFullCard && !hasCvv;
    }
});

// ── Check 2: Logging ──────────────────────────────────────────────────
Console.WriteLine("─── Data in Logs ───");
RunCheck("Logs do NOT contain full card numbers or SSNs", () =>
{
    var svc = new CustomerService();
    svc.LogTransaction("4111222233334444", "123-45-6789", 99.99m);
    string log = svc.LogOutput[0];
    bool hasFullCard = log.Contains("4111222233334444");
    bool hasFullSsn = log.Contains("123-45-6789");
    return !hasFullCard && !hasFullSsn;
});

// ── Check 3: ToString ─────────────────────────────────────────────────
Console.WriteLine("─── Data in ToString ───");
RunCheck("Customer.ToString() does NOT include SSN or Password", () =>
{
    var customer = new Customer { Name = "Alice", Email = "a@b.com", SSN = "123-45-6789", Password = "secret123", CardNumber = "4111222233334444" };
    string str = customer.ToString();
    return !str.Contains("123-45-6789") && !str.Contains("secret123");
});

// ── Check 4: File storage ─────────────────────────────────────────────
Console.WriteLine("─── Data at Rest ───");
RunCheck("Saved data does NOT contain plaintext passwords", () =>
{
    var customer = new Customer { Name = "Alice", Email = "a@b.com", SSN = "123-45-6789", Password = "secret123", CardNumber = "4111222233334444" };
    string json = service.SaveCustomerData(customer);
    return !json.Contains("secret123");
});

// ── Check 5: URL credentials ─────────────────────────────────────────
Console.WriteLine("─── Data in Transit ───");
RunCheck("API URL does NOT contain credentials in query string", () =>
{
    var (url, headers) = service.BuildApiUrl("sk-live-key123", "user42");
    bool urlHasKey = url.Contains("sk-live-key123");
    bool headersHaveKey = headers.ContainsKey("Authorization") || headers.ContainsKey("X-Api-Key");
    return !urlHasKey && headersHaveKey;
});

// ── Check 6: Memory cleanup ──────────────────────────────────────────
Console.WriteLine("─── Data in Memory ───");
RunCheck("Sensitive byte arrays are zeroed after use", () =>
{
    var svc = new CustomerService();
    svc.ProcessSensitiveInput("TestPassword123");
    return svc.WasSensitiveDataCleared;
});

Console.WriteLine();
Console.WriteLine("══════════════════════════════════════════════════════════");
if (failed == 0) { Console.ForegroundColor = ConsoleColor.Green; Console.WriteLine($"  ALL {passed} CHECKS PASSED — Data handling is secure! 🔒"); }
else { Console.ForegroundColor = ConsoleColor.Yellow; Console.WriteLine($"  {passed} passed, {failed} failed — {failed} vulnerability(ies) remaining."); Console.WriteLine("  Fix the vulnerabilities and run again: dotnet run"); }
Console.ResetColor();
Console.WriteLine("══════════════════════════════════════════════════════════");
Console.WriteLine();
