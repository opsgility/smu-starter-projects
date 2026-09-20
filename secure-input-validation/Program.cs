// =============================================================================
//  SECURE INPUT VALIDATION — Security Challenge
// =============================================================================
//
//  This program contains INTENTIONALLY VULNERABLE code.
//  There are 6 security vulnerabilities in UserRepository.cs and CommandRunner.cs.
//
//  YOUR MISSION: Find and fix all 6 security vulnerabilities.
//
//  How to run:   dotnet run
//
//  The program runs security checks. Each prints PASS or FAIL.
//  When all 6 vulnerabilities are fixed, every check will print PASS.
//
//  The vulnerabilities are in UserRepository.cs and CommandRunner.cs — NOT here.
//
//  Good luck, Security Engineer!
// =============================================================================

using Microsoft.Data.Sqlite;

// Set up in-memory SQLite database
var connection = new SqliteConnection("Data Source=:memory:");
connection.Open();

// Create and seed the test database
var setupCmd = connection.CreateCommand();
setupCmd.CommandText = @"
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        name TEXT NOT NULL,
        email TEXT NOT NULL
    );
    INSERT INTO users VALUES (1, 'admin', 'secret123', 'Admin User', 'admin@example.com');
    INSERT INTO users VALUES (2, 'alice', 'password1', 'Alice Johnson', 'alice@example.com');
    INSERT INTO users VALUES (3, 'bob', 'pass456', 'Bob Smith', 'bob@example.com');
    INSERT INTO users VALUES (4, 'charlie', 'qwerty', 'Charlie Brown', 'charlie@example.com');
";
setupCmd.ExecuteNonQuery();

var repo = new UserRepository(connection);
var runner = new CommandRunner();

Console.WriteLine("╔══════════════════════════════════════════════════════════╗");
Console.WriteLine("║        SECURE INPUT VALIDATION — Security Challenge     ║");
Console.WriteLine("║        Find and fix all 6 vulnerabilities!              ║");
Console.WriteLine("╚══════════════════════════════════════════════════════════╝");
Console.WriteLine();

int passed = 0;
int failed = 0;

void RunCheck(string name, Func<bool> check)
{
    try
    {
        bool result = check();
        if (result)
        {
            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine($"  ✓ PASS  {name}");
            passed++;
        }
        else
        {
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine($"  ✗ FAIL  {name}");
            failed++;
        }
    }
    catch (Exception ex)
    {
        Console.ForegroundColor = ConsoleColor.Red;
        Console.WriteLine($"  ✗ CRASH {name}");
        Console.ForegroundColor = ConsoleColor.DarkRed;
        Console.WriteLine($"          {ex.GetType().Name}: {ex.Message}");
        failed++;
    }
    Console.ResetColor();
}

// ── Check 1: SQL Injection in Login ──────────────────────────────────────
Console.WriteLine("─── SQL Injection Prevention ───");

RunCheck("Login resists SQL injection (auth bypass)", () =>
{
    // This SQL injection payload should NOT return a valid user
    var result = repo.Authenticate("' OR '1'='1", "' OR '1'='1");
    return result == null; // Should be null — attack blocked
});

// ── Check 2: SQL Injection in Search ─────────────────────────────────────
RunCheck("Search resists SQL injection (data extraction)", () =>
{
    // This should NOT return all users — just ones matching the literal search
    var results = repo.SearchUsers("' OR '1'='1");
    return results.Count == 0; // Injection should find nothing
});

// ── Check 3: Command Injection ──────────────────────────────────────────
Console.WriteLine("─── Command Injection Prevention ───");

RunCheck("Hostname validation blocks command injection", () =>
{
    // This should be rejected — it contains shell metacharacters
    bool blocked = false;
    try
    {
        runner.Ping("127.0.0.1; rm -rf /");
        blocked = false; // If it ran without error, injection wasn't blocked
    }
    catch (ArgumentException)
    {
        blocked = true; // Correctly rejected
    }
    return blocked;
});

// ── Check 4: Input Length Validation ─────────────────────────────────────
Console.WriteLine("─── Input Validation ───");

RunCheck("Username length is validated (max 50 chars)", () =>
{
    bool blocked = false;
    try
    {
        var longUsername = new string('A', 1000); // 1000-char username
        repo.CreateUser(longUsername, "password", "Test User", "test@example.com");
        blocked = false;
    }
    catch (ArgumentException)
    {
        blocked = true; // Correctly rejected
    }
    return blocked;
});

// ── Check 5: HTML Encoding ───────────────────────────────────────────────
RunCheck("Output is HTML-encoded (XSS prevention)", () =>
{
    string maliciousName = "<script>alert('xss')</script>";
    string output = repo.FormatUserProfile(maliciousName, "hacker@evil.com");
    // The output should NOT contain raw <script> tags
    return !output.Contains("<script>") && output.Contains("&lt;script&gt;");
});

// ── Check 6: Path Injection ──────────────────────────────────────────────
Console.WriteLine("─── Path Injection Prevention ───");

RunCheck("Export filename blocks path traversal", () =>
{
    bool blocked = false;
    try
    {
        repo.ExportUserData("../../etc/passwd", "some data");
        blocked = false;
    }
    catch (ArgumentException)
    {
        blocked = true; // Correctly rejected
    }
    return blocked;
});

// ── Final Report ────────────────────────────────────────────────────────
Console.WriteLine();
Console.WriteLine("══════════════════════════════════════════════════════════");
if (failed == 0)
{
    Console.ForegroundColor = ConsoleColor.Green;
    Console.WriteLine($"  ALL {passed} CHECKS PASSED — Code is secure! 🔒");
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
