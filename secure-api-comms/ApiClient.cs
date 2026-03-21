using System.Net.Http.Headers;

/// <summary>
/// API client with INTENTIONALLY VULNERABLE HTTP communication.
/// </summary>
public class ApiClient
{
    private readonly HttpClient _client;

    /// <summary>
    /// BUG #1: Disables SSL certificate validation.
    /// FIX: Remove the ServerCertificateCustomValidationCallback entirely.
    /// BUG #5: No timeout set on HttpClient.
    /// FIX: Set Timeout to TimeSpan.FromSeconds(30).
    /// </summary>
    public ApiClient()
    {
        var handler = new HttpClientHandler();

        // ⚠️ VULNERABILITY #1: Accepting ANY certificate (MITM risk)
        handler.ServerCertificateCustomValidationCallback = (_, _, _, _) => true;

        _client = new HttpClient(handler);
        // ⚠️ VULNERABILITY #5: No timeout (defaults to 100 seconds)
    }

    /// <summary>
    /// Check if SSL validation is properly configured.
    /// </summary>
    public bool HasCertificateValidationDisabled()
    {
        // Returns true if the dangerous callback is set
        // After fix, this should return false
        return true; // ⚠️ Indicates validation is disabled
    }

    /// <summary>
    /// BUG #2: Uses HTTP instead of HTTPS.
    /// FIX: Change to https:// and add a guard that throws on http://.
    /// </summary>
    public string GetDataUrl()
    {
        // ⚠️ VULNERABILITY: HTTP instead of HTTPS
        return "http://api.example.com/data";
    }

    /// <summary>
    /// BUG #3: Puts API key and secret in URL query parameters.
    /// FIX: Return credentials in a headers dictionary, not in the URL.
    /// </summary>
    public (string Url, Dictionary<string, string> Headers) Authenticate(string apiKey, string secret)
    {
        // ⚠️ VULNERABILITY: Secrets in URL query parameters
        string url = $"https://api.example.com/auth?api_key={apiKey}&secret={secret}";
        return (url, new Dictionary<string, string>());
    }

    /// <summary>
    /// BUG #6: User input concatenated into URL without encoding.
    /// FIX: Use Uri.EscapeDataString(userInput).
    /// </summary>
    public string BuildSearchUrl(string userInput)
    {
        // ⚠️ VULNERABILITY: Unencoded user input in URL
        return $"https://api.example.com/search?q={userInput}";
    }

    /// <summary>
    /// Get the configured timeout.
    /// </summary>
    public TimeSpan GetTimeout() => _client.Timeout;
}
