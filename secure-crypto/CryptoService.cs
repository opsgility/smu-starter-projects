using System.Security.Cryptography;
using System.Text;

/// <summary>
/// Cryptography service with INTENTIONALLY VULNERABLE code.
/// Find and fix all 6 security vulnerabilities.
/// </summary>
public class CryptoService
{
    /// <summary>
    /// BUG #5: Hardcoded encryption key.
    /// FIX: Load from Environment.GetEnvironmentVariable("ENCRYPTION_KEY").
    /// </summary>
    public byte[] GetEncryptionKey()
    {
        // ⚠️ VULNERABILITY: Hardcoded key in source code
        return Encoding.UTF8.GetBytes("ThisIsMySecretKey1234567890123456");
    }

    /// <summary>
    /// Encrypt data with AES.
    /// BUG #1: Uses ECB mode — patterns visible in ciphertext.
    /// FIX: Use CipherMode.CBC with aes.GenerateIV(), prepend IV to output.
    /// BUG #2: Uses a static all-zeros IV.
    /// FIX: Generate a fresh IV per encryption with aes.GenerateIV().
    /// BUG #6: Returns raw ciphertext with no integrity check.
    /// FIX: Add HMAC-SHA256 over the ciphertext, or use AesGcm.
    /// </summary>
    public byte[] Encrypt(byte[] plaintext, byte[] key)
    {
        using var aes = Aes.Create();
        aes.Key = key;

        // ⚠️ VULNERABILITY #1: ECB mode — patterns visible
        aes.Mode = CipherMode.ECB;

        // ⚠️ VULNERABILITY #2: Static IV (all zeros) — reused for every encryption
        aes.IV = new byte[16];

        using var encryptor = aes.CreateEncryptor();
        // ⚠️ VULNERABILITY #6: No HMAC — ciphertext can be tampered with
        return encryptor.TransformFinalBlock(plaintext, 0, plaintext.Length);
    }

    /// <summary>
    /// Decrypt data with AES (matches the Encrypt method).
    /// </summary>
    public byte[] Decrypt(byte[] ciphertext, byte[] key)
    {
        using var aes = Aes.Create();
        aes.Key = key;
        aes.Mode = CipherMode.ECB;
        aes.IV = new byte[16];
        using var decryptor = aes.CreateDecryptor();
        return decryptor.TransformFinalBlock(ciphertext, 0, ciphertext.Length);
    }

    /// <summary>
    /// Store a password securely.
    /// BUG #3: ENCRYPTS passwords instead of HASHING them.
    /// FIX: Use SHA256 or PBKDF2 hashing — passwords should be one-way.
    /// Return a hash string, not encrypted bytes.
    /// </summary>
    public byte[] StorePasswordHash(string password, byte[] key)
    {
        // ⚠️ VULNERABILITY: Using encryption (reversible) for passwords
        // Passwords should be HASHED (one-way), not encrypted (two-way)
        byte[] passwordBytes = Encoding.UTF8.GetBytes(password);
        return Encrypt(passwordBytes, key);
    }

    /// <summary>
    /// Verify a stored password against input.
    /// Should work with whatever StorePasswordHash returns.
    /// </summary>
    public bool VerifyPassword(string inputPassword, byte[] storedHash, byte[] key)
    {
        // This currently decrypts and compares — should use hash comparison
        byte[] decrypted = Decrypt(storedHash, key);
        string stored = Encoding.UTF8.GetString(decrypted).TrimEnd('\0');
        return stored == inputPassword;
    }

    /// <summary>
    /// Protect a credit card number for storage.
    /// BUG #4: HASHES the credit card — data is destroyed and unrecoverable.
    /// FIX: Use AES encryption so the card number can be retrieved when needed.
    /// </summary>
    public string ProtectCreditCard(string cardNumber)
    {
        // ⚠️ VULNERABILITY: Hashing (one-way) when encryption (two-way) is needed
        // Credit card numbers need to be RECOVERABLE for processing
        byte[] cardBytes = Encoding.UTF8.GetBytes(cardNumber);
        byte[] hash = SHA256.HashData(cardBytes);
        return Convert.ToHexString(hash);
    }

    /// <summary>
    /// Recover a protected credit card number.
    /// Should return the original card number if ProtectCreditCard used encryption.
    /// </summary>
    public string RecoverCreditCard(string protectedCard, byte[] key)
    {
        // Currently impossible — SHA256 hash can't be reversed
        // After fix: should decrypt and return original card number
        return "UNRECOVERABLE";
    }
}
