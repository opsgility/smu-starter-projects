// =============================================================================
//  SECURE CRYPTOGRAPHY — Security Challenge
// =============================================================================
//  6 cryptography vulnerabilities in CryptoService.cs.
//  Run: dotnet run
//  Fix all 6 to make every check PASS.
// =============================================================================

using System.Security.Cryptography;
using System.Text;

Environment.SetEnvironmentVariable("ENCRYPTION_KEY", "TestKeyFromEnv!1234567890123456");

var crypto = new CryptoService();

Console.WriteLine("╔══════════════════════════════════════════════════════════╗");
Console.WriteLine("║        SECURE CRYPTOGRAPHY — Security Challenge         ║");
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
        if (result) { Console.ForegroundColor = ConsoleColor.Green; Console.WriteLine($"  ✓ PASS  {name}"); passed++; }
        else { Console.ForegroundColor = ConsoleColor.Red; Console.WriteLine($"  ✗ FAIL  {name}"); failed++; }
    }
    catch (Exception ex) { Console.ForegroundColor = ConsoleColor.Red; Console.WriteLine($"  ✗ CRASH {name}"); Console.ForegroundColor = ConsoleColor.DarkRed; Console.WriteLine($"          {ex.GetType().Name}: {ex.Message}"); failed++; }
    Console.ResetColor();
}

byte[] key = crypto.GetEncryptionKey();

// ── Check 1: Not ECB Mode ─────────────────────────────────────────────
Console.WriteLine("─── Encryption Mode ───");
RunCheck("Encryption does NOT use ECB mode (identical blocks differ)", () =>
{
    // ECB: identical plaintext blocks → identical ciphertext blocks
    byte[] block = Encoding.UTF8.GetBytes("AAAAAAAAAAAAAAAA"); // 16 bytes
    byte[] doubleBlock = new byte[32];
    Array.Copy(block, 0, doubleBlock, 0, 16);
    Array.Copy(block, 0, doubleBlock, 16, 16);
    byte[] encrypted = crypto.Encrypt(doubleBlock, key);
    // In ECB, bytes 0-15 == bytes 16-31. In CBC, they differ.
    bool firstBlock = encrypted.Take(16).ToArray().SequenceEqual(encrypted.Skip(16).Take(16).ToArray());
    return !firstBlock; // Should be different (NOT ECB)
});

// ── Check 2: Unique IVs ──────────────────────────────────────────────
RunCheck("Different encryptions produce different ciphertext (unique IVs)", () =>
{
    byte[] data = Encoding.UTF8.GetBytes("Same plaintext!!");
    byte[] enc1 = crypto.Encrypt(data, key);
    byte[] enc2 = crypto.Encrypt(data, key);
    return !enc1.SequenceEqual(enc2); // Should differ due to random IV
});

// ── Check 3: Passwords are hashed, not encrypted ─────────────────────
Console.WriteLine("─── Correct Primitive ───");
RunCheck("Passwords are HASHED (one-way), not encrypted", () =>
{
    byte[] stored = crypto.StorePasswordHash("MyPassword123", key);
    // If properly hashed, trying to "decrypt" should fail or be meaningless
    // Also, the verify method should work without decryption
    bool verifyWorks = crypto.VerifyPassword("MyPassword123", stored, key);
    bool wrongFails = !crypto.VerifyPassword("WrongPassword", stored, key);
    // Check that stored hash is NOT the same as AES encryption of the password
    byte[] aesEncrypted = crypto.Encrypt(Encoding.UTF8.GetBytes("MyPassword123"), key);
    bool notAes = !stored.SequenceEqual(aesEncrypted);
    return verifyWorks && wrongFails && notAes;
});

// ── Check 4: Credit cards are encrypted, not hashed ───────────────────
RunCheck("Credit cards are ENCRYPTED (recoverable), not hashed", () =>
{
    string card = "4111111111111111";
    string protected_ = crypto.ProtectCreditCard(card);
    string recovered = crypto.RecoverCreditCard(protected_, key);
    return recovered == card; // Must be recoverable
});

// ── Check 5: Key from environment ─────────────────────────────────────
Console.WriteLine("─── Key Management ───");
RunCheck("Encryption key loaded from environment variable", () =>
{
    byte[] envKey = crypto.GetEncryptionKey();
    byte[] hardcoded = Encoding.UTF8.GetBytes("ThisIsMySecretKey1234567890123456");
    return !envKey.SequenceEqual(hardcoded); // Should NOT be the hardcoded value
});

// ── Check 6: Authenticated encryption ─────────────────────────────────
RunCheck("Ciphertext includes authentication (HMAC or GCM)", () =>
{
    byte[] data = Encoding.UTF8.GetBytes("Test data here!!");
    byte[] encrypted = crypto.Encrypt(data, key);
    // Authenticated encryption output is LARGER than raw ciphertext
    // Raw AES of 16 bytes = 16 or 32 bytes. With HMAC = +32 bytes. With IV = +16 bytes.
    // So authenticated + IV output should be > 48 bytes for 16 bytes of plaintext
    return encrypted.Length > 48;
});

Console.WriteLine();
Console.WriteLine("══════════════════════════════════════════════════════════");
if (failed == 0) { Console.ForegroundColor = ConsoleColor.Green; Console.WriteLine($"  ALL {passed} CHECKS PASSED — Cryptography is secure! 🔒"); }
else { Console.ForegroundColor = ConsoleColor.Yellow; Console.WriteLine($"  {passed} passed, {failed} failed — {failed} vulnerability(ies) remaining."); Console.WriteLine("  Fix the vulnerabilities and run again: dotnet run"); }
Console.ResetColor();
Console.WriteLine("══════════════════════════════════════════════════════════");
Console.WriteLine();
