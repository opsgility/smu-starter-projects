// =============================================================================
//  SECURITY AUDIT CAPSTONE — Find and Fix 10 Vulnerabilities
// =============================================================================
//  UserManagementApp.cs contains 10 security vulnerabilities from all 7 lessons.
//  Run: dotnet run
//  Fix all 10 to pass the complete security audit.
// =============================================================================

using Microsoft.Data.Sqlite;
using System.Security.Cryptography;
using System.Text;

// Setup
Environment.SetEnvironmentVariable("API_KEY", "sk-test-capstone-env-key");
var connection = new SqliteConnection("Data Source=:memory:");
connection.Open();
var setup = connection.CreateCommand();
setup.CommandText = @"
    CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, name TEXT);
    INSERT INTO users VALUES (1, 'admin', 'admin123', 'Admin User');
    INSERT INTO users VALUES (2, 'alice', 'password1', 'Alice Johnson');
    INSERT INTO users VALUES (3, 'bob', 'bobpass', 'Bob Smith');
";
setup.ExecuteNonQuery();

var app = new UserManagementApp(connection);

Console.WriteLine("╔══════════════════════════════════════════════════════════╗");
Console.WriteLine("║        SECURITY AUDIT CAPSTONE — 10 Vulnerabilities     ║");
Console.WriteLine("║        Find and fix ALL 10 to pass the audit!           ║");
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

byte[] testKey = Encoding.UTF8.GetBytes("TestCapstoneKey!1234567890123456");

// ── 1. SQL Injection ──────────────────────────────────────────────────
Console.WriteLine("─── Injection (L1) ───");
RunCheck("#1  Search resists SQL injection", () =>
{
    var results = app.SearchUsers("' OR '1'='1");
    return results.Count == 0;
});

// ── 2. Plaintext Password Storage ─────────────────────────────────────
Console.WriteLine("─── Authentication (L2) ───");
RunCheck("#2  Passwords are hashed, not plaintext", () =>
{
    // Re-setup for this test
    var testConn = new SqliteConnection("Data Source=:memory:");
    testConn.Open();
    var s = testConn.CreateCommand();
    s.CommandText = "CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, name TEXT);";
    s.ExecuteNonQuery();
    var testApp = new UserManagementApp(testConn);
    testApp.RegisterUser("testuser", "MyPassword!", "Test");

    // Read what was stored
    var cmd = testConn.CreateCommand();
    cmd.CommandText = "SELECT password FROM users WHERE username='testuser'";
    string? stored = cmd.ExecuteScalar()?.ToString();
    testConn.Close();

    return stored != "MyPassword!"; // Should be hashed, not plaintext
});

// ── 3. Password Comparison ────────────────────────────────────────────
RunCheck("#3  Login uses BCrypt.Verify, not ==", () =>
{
    var testConn = new SqliteConnection("Data Source=:memory:");
    testConn.Open();
    var s = testConn.CreateCommand();
    s.CommandText = "CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, name TEXT);";
    s.ExecuteNonQuery();
    var testApp = new UserManagementApp(testConn);
    testApp.RegisterUser("alice2", "SecurePass!", "Alice");
    bool correct = testApp.Login("alice2", "SecurePass!");
    bool wrong = testApp.Login("alice2", "WrongPass");
    testConn.Close();
    return correct && !wrong;
});

// ── 4. Encryption Mode ───────────────────────────────────────────────
Console.WriteLine("─── Cryptography (L3) ───");
RunCheck("#4  Encryption does NOT use ECB mode", () =>
{
    byte[] block = Encoding.UTF8.GetBytes("AAAAAAAAAAAAAAAA");
    byte[] doubleBlock = new byte[32];
    Array.Copy(block, 0, doubleBlock, 0, 16);
    Array.Copy(block, 0, doubleBlock, 16, 16);
    byte[] enc = app.EncryptUserData(Encoding.UTF8.GetString(doubleBlock), testKey);
    bool ecb = enc.Take(16).SequenceEqual(enc.Skip(16).Take(16));
    return !ecb;
});

// ── 5. Sensitive Data in Logs ────────────────────────────────────────
Console.WriteLine("─── Data Handling (L4) ───");
RunCheck("#5  Logs do NOT contain passwords or tokens", () =>
{
    var testApp2 = new UserManagementApp(connection);
    testApp2.LogActivity("alice", "SecretPass123", "login");
    return testApp2.LogOutput.All(l => !l.Contains("SecretPass123") && !l.Contains("sk-prod-realkey"));
});

// ── 6. Path Traversal ────────────────────────────────────────────────
Console.WriteLine("─── File Security (L5) ───");
RunCheck("#6  Export blocks path traversal", () =>
{
    bool blocked = false;
    try { app.ExportData("../../evil.txt", "malicious"); }
    catch (ArgumentException) { blocked = true; }
    return blocked;
});

// ── 7. Hardcoded API Key ─────────────────────────────────────────────
Console.WriteLine("─── Secrets (L6) ───");
RunCheck("#7  API key is NOT hardcoded", () =>
{
    string key = app.GetApiKey();
    return key != "sk-prod-realkey123secretvalue";
});

// ── 8. SSL Validation ────────────────────────────────────────────────
Console.WriteLine("─── API Security (L7) ───");
RunCheck("#8  SSL certificate validation is enabled", () =>
{
    return !app.HasSslValidationDisabled();
});

// ── 9. Input Validation ──────────────────────────────────────────────
Console.WriteLine("─── Input Validation (L1) ───");
RunCheck("#9  Username length is validated", () =>
{
    bool blocked = false;
    try
    {
        var testConn = new SqliteConnection("Data Source=:memory:");
        testConn.Open();
        var s = testConn.CreateCommand();
        s.CommandText = "CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, name TEXT);";
        s.ExecuteNonQuery();
        var testApp = new UserManagementApp(testConn);
        testApp.RegisterUser(new string('A', 500), "pass", "name");
        testConn.Close();
    }
    catch (ArgumentException) { blocked = true; }
    return blocked;
});

// ── 10. Credentials in URL ───────────────────────────────────────────
Console.WriteLine("─── Secrets in Transit (L6/L7) ───");
RunCheck("#10 Credentials NOT in URL query parameters", () =>
{
    var (url, headers) = app.BuildExternalUrl("sk-key-123", "user42");
    bool urlClean = !url.Contains("sk-key-123");
    bool headersHaveAuth = headers.ContainsKey("Authorization") || headers.ContainsKey("X-Api-Key");
    return urlClean && headersHaveAuth;
});

// ── Final Report ─────────────────────────────────────────────────────
Console.WriteLine();
Console.WriteLine("══════════════════════════════════════════════════════════");
if (failed == 0)
{
    Console.ForegroundColor = ConsoleColor.Green;
    Console.WriteLine($"  ALL {passed} CHECKS PASSED — Security audit complete! 🔒🏆");
    Console.WriteLine("  Tell the code assistant: 'Review my code' for your grade.");
}
else
{
    Console.ForegroundColor = ConsoleColor.Yellow;
    Console.WriteLine($"  {passed} passed, {failed} failed — {failed} vulnerability(ies) remaining.");
    Console.WriteLine("  Fix the vulnerabilities and run again: dotnet run");
}
Console.ResetColor();
Console.WriteLine("══════════════════════════════════════════════════════════");
Console.WriteLine();

connection.Close();
