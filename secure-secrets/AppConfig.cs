using System.Diagnostics;
using System.Text;

/// <summary>
/// Application configuration with INTENTIONALLY VULNERABLE secrets management.
/// </summary>
public class AppConfig
{
    /// <summary>
    /// BUG #2: Hardcoded API key as a constant.
    /// FIX: Read from Environment.GetEnvironmentVariable("API_KEY") or IConfiguration.
    /// </summary>
    public const string ApiKey = "sk-live-abc123def456";

    /// <summary>
    /// Get the API key.
    /// Should read from environment/config, not from the hardcoded const.
    /// </summary>
    public string GetApiKey()
    {
        return ApiKey; // ⚠️ Returns hardcoded const
    }

    /// <summary>
    /// Get API request headers.
    /// BUG #5: Debug.WriteLine exposes the API key.
    /// FIX: Remove the Debug output.
    /// </summary>
    public Dictionary<string, string> GetApiHeaders()
    {
        // ⚠️ VULNERABILITY: API key leaked to debug output
        Debug.WriteLine($"Using key: {ApiKey}");

        return new Dictionary<string, string>
        {
            ["Authorization"] = $"Bearer {GetApiKey()}",
            ["Content-Type"] = "application/json"
        };
    }

    /// <summary>
    /// Load an "encrypted" configuration.
    /// BUG #6: Base64 decode is NOT encryption — it's just encoding.
    /// FIX: Implement real AES decryption or use .NET User Secrets.
    /// </summary>
    public string LoadEncryptedConfig(string base64Value)
    {
        // ⚠️ VULNERABILITY: Base64 is encoding, not encryption
        // Anyone can decode it — it provides zero security
        byte[] bytes = Convert.FromBase64String(base64Value);
        return Encoding.UTF8.GetString(bytes);
    }

    /// <summary>
    /// Check if the "encryption" is real encryption (not just Base64).
    /// </summary>
    public bool IsRealEncryption(string original, string encrypted)
    {
        // If it's just Base64, decoding gives back the original
        try
        {
            string decoded = Encoding.UTF8.GetString(Convert.FromBase64String(encrypted));
            return decoded != original; // Real encryption won't decode to original via Base64
        }
        catch
        {
            return true; // If Base64 decode fails, it's not Base64 = probably real encryption
        }
    }
}
