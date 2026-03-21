using System.Security.Cryptography;
using System.Text;

/// <summary>
/// Authentication service with INTENTIONALLY VULNERABLE code.
/// Find and fix all 6 security vulnerabilities.
/// </summary>
public class AuthService
{
    private Dictionary<string, string> _users = new();
    private Dictionary<string, int> _failedAttempts = new();
    private Dictionary<string, DateTime> _lockouts = new();

    // A "secret" API key for service-to-service auth
    private const string ValidApiKey = "sk-prod-abc123def456ghi789";

    /// <summary>
    /// Register a new user.
    /// BUG #1: Stores password in PLAINTEXT.
    /// FIX: Use BCrypt.Net.BCrypt.HashPassword(password) to hash before storing.
    /// </summary>
    public void RegisterUser(string username, string password)
    {
        // ⚠️ VULNERABILITY: Plaintext password storage
        _users[username] = password;
    }

    /// <summary>
    /// Login a user.
    /// BUG #2: Compares passwords with == (plaintext comparison).
    /// FIX: Use BCrypt.Net.BCrypt.Verify(inputPassword, storedHash).
    /// BUG #6: No brute-force protection — unlimited attempts.
    /// FIX: Track failed attempts, lock account after 5 failures for 15 minutes.
    /// </summary>
    public bool Login(string username, string password)
    {
        if (!_users.ContainsKey(username)) return false;

        // ⚠️ VULNERABILITY #6: No account lockout
        // TODO: Check if account is locked out before proceeding

        // ⚠️ VULNERABILITY #2: Plaintext comparison
        if (_users[username] == password)
        {
            return true;
        }

        // TODO: Track failed attempt count, lock after 5 failures
        return false;
    }

    /// <summary>
    /// Hash a password.
    /// BUG #3: Uses MD5 — a BROKEN hash algorithm.
    /// FIX: Replace with BCrypt.Net.BCrypt.HashPassword() or PBKDF2.
    /// </summary>
    public string HashPassword(string password)
    {
        // ⚠️ VULNERABILITY: MD5 is broken — cracked in seconds with rainbow tables
        using var md5 = MD5.Create();
        byte[] hash = md5.ComputeHash(Encoding.UTF8.GetBytes(password));
        return Convert.ToHexString(hash);
    }

    /// <summary>
    /// Hash a password with a salt.
    /// BUG #4: Uses a HARDCODED salt — defeats the purpose of salting.
    /// FIX: Generate a cryptographically random salt with RandomNumberGenerator.GetBytes(16).
    /// </summary>
    public string HashWithSalt(string password)
    {
        // ⚠️ VULNERABILITY: Hardcoded salt — same salt for every user
        byte[] salt = Encoding.UTF8.GetBytes("mysalt123");

        using var hmac = new HMACSHA256(salt);
        byte[] hash = hmac.ComputeHash(Encoding.UTF8.GetBytes(password));
        return Convert.ToHexString(hash);
    }

    /// <summary>
    /// Returns a random salt. Used by the security check to verify proper salt generation.
    /// </summary>
    public byte[] GenerateSalt()
    {
        // ⚠️ This should use RandomNumberGenerator, not a hardcoded value
        return Encoding.UTF8.GetBytes("mysalt123");
    }

    /// <summary>
    /// Validate an API key.
    /// BUG #5: Character-by-character comparison with early return — TIMING ATTACK.
    /// FIX: Use CryptographicOperations.FixedTimeEquals() for constant-time comparison.
    /// </summary>
    public bool ValidateApiKey(string inputKey)
    {
        if (inputKey.Length != ValidApiKey.Length) return false;

        // ⚠️ VULNERABILITY: Timing attack — early return reveals info
        for (int i = 0; i < ValidApiKey.Length; i++)
        {
            if (inputKey[i] != ValidApiKey[i])
                return false; // Returns faster when first chars are wrong
        }
        return true;
    }
}
