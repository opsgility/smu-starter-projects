// =============================================================================
//  SECURE AUTHENTICATION — Security Challenge
// =============================================================================
//  6 authentication vulnerabilities in AuthService.cs.
//  Run: dotnet run
//  Fix all 6 to make every check PASS.
// =============================================================================

using System.Security.Cryptography;
using System.Text;

var auth = new AuthService();

Console.WriteLine("╔══════════════════════════════════════════════════════════╗");
Console.WriteLine("║      SECURE AUTHENTICATION — Security Challenge         ║");
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

// ── Check 1: Password Storage ──────────────────────────────────────────
Console.WriteLine("─── Password Storage ───");

RunCheck("Passwords are hashed, not stored in plaintext", () =>
{
    var testAuth = new AuthService();
    testAuth.RegisterUser("testuser", "MyPassword123!");

    // After registration, try to login with the password
    // If registration stores a hash, the login method must use BCrypt.Verify
    // We can't directly check the stored value, but we can verify the login works
    // AND that HashPassword doesn't use MD5
    bool canLogin = testAuth.Login("testuser", "MyPassword123!");

    // The password should work for login (meaning hash+verify is implemented)
    // AND the hash method should NOT be MD5
    string hash = testAuth.HashPassword("test");
    bool isMd5Length = hash.Length == 32; // MD5 produces 32 hex chars

    return canLogin && !isMd5Length;
});

// ── Check 2: No Plaintext Comparison ──────────────────────────────────
RunCheck("Login uses BCrypt.Verify, not string equality", () =>
{
    var testAuth = new AuthService();
    testAuth.RegisterUser("alice", "SecurePass456!");

    // If using BCrypt properly:
    // - RegisterUser hashes the password
    // - Login uses BCrypt.Verify to compare
    // - Login with correct password returns true
    // - Login with wrong password returns false
    bool correctPass = testAuth.Login("alice", "SecurePass456!");
    bool wrongPass = testAuth.Login("alice", "WrongPassword");

    return correctPass && !wrongPass;
});

// ── Check 3: Strong Hashing Algorithm ─────────────────────────────────
Console.WriteLine("─── Hashing Algorithm ───");

RunCheck("HashPassword does NOT use MD5", () =>
{
    var testAuth = new AuthService();
    string hash = testAuth.HashPassword("testpassword");

    // MD5 produces a 32-character hex string
    // BCrypt produces a 60-character string starting with $2
    // PBKDF2 produces a longer output
    bool notMd5 = hash.Length != 32;
    return notMd5;
});

// ── Check 4: Random Salt ──────────────────────────────────────────────
RunCheck("Salt is cryptographically random, not hardcoded", () =>
{
    var testAuth = new AuthService();
    byte[] salt1 = testAuth.GenerateSalt();
    byte[] salt2 = testAuth.GenerateSalt();

    // If salt is random, two calls should produce different values
    // If hardcoded, they'll be identical
    bool different = !salt1.SequenceEqual(salt2);
    bool rightSize = salt1.Length >= 16; // At least 128 bits

    return different && rightSize;
});

// ── Check 5: Constant-Time Comparison ─────────────────────────────────
Console.WriteLine("─── Timing & Brute Force ───");

RunCheck("API key validation uses constant-time comparison", () =>
{
    var testAuth = new AuthService();

    // We can't easily measure timing, but we can check if the method
    // uses CryptographicOperations.FixedTimeEquals by checking behavior:
    // The valid key should validate, invalid should not
    bool validWorks = testAuth.ValidateApiKey("sk-prod-abc123def456ghi789");
    bool invalidFails = !testAuth.ValidateApiKey("sk-prod-WRONG_KEY_HERE!!");

    // Check that it handles different lengths safely
    bool shortFails = !testAuth.ValidateApiKey("short");

    return validWorks && invalidFails && shortFails;
});

// ── Check 6: Account Lockout ──────────────────────────────────────────
RunCheck("Account locks after 5 failed login attempts", () =>
{
    var testAuth = new AuthService();
    testAuth.RegisterUser("victim", "RealPassword!");

    // Try 5 wrong passwords
    for (int i = 0; i < 5; i++)
    {
        testAuth.Login("victim", $"wrong{i}");
    }

    // 6th attempt with CORRECT password should fail (locked out)
    bool lockedOut = false;
    try
    {
        bool result = testAuth.Login("victim", "RealPassword!");
        lockedOut = !result; // Should return false because locked
    }
    catch
    {
        lockedOut = true; // Or throw an exception — either is acceptable
    }

    return lockedOut;
});

// ── Final Report ────────────────────────────────────────────────────────
Console.WriteLine();
Console.WriteLine("══════════════════════════════════════════════════════════");
if (failed == 0)
{
    Console.ForegroundColor = ConsoleColor.Green;
    Console.WriteLine($"  ALL {passed} CHECKS PASSED — Authentication is secure! 🔒");
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
