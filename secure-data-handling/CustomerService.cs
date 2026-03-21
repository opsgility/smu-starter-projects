using System.Security.Cryptography;
using System.Text;
using System.Text.Json;

public class Customer
{
    public string Name { get; set; } = "";
    public string Email { get; set; } = "";
    public string SSN { get; set; } = "";
    public string Password { get; set; } = "";
    public string CardNumber { get; set; } = "";

    /// <summary>
    /// BUG #3: ToString() includes SSN and Password — these leak everywhere.
    /// FIX: Exclude sensitive fields or mask them.
    /// </summary>
    public override string ToString()
    {
        // ⚠️ VULNERABILITY: Sensitive data in ToString
        return $"Customer: {Name}, Email: {Email}, SSN: {SSN}, Password: {Password}";
    }
}

/// <summary>
/// Customer service with INTENTIONALLY VULNERABLE data handling.
/// Find and fix all 6 security vulnerabilities.
/// </summary>
public class CustomerService
{
    private readonly List<string> _logOutput = new();

    public IReadOnlyList<string> LogOutput => _logOutput;

    /// <summary>
    /// Process a payment.
    /// BUG #1: Exception message contains full card number and CVV.
    /// FIX: Mask card to last 4 digits, never include CVV.
    /// </summary>
    public void ProcessPayment(string cardNumber, string cvv, decimal amount)
    {
        if (amount <= 0)
        {
            // ⚠️ VULNERABILITY: Full card number and CVV in exception
            throw new Exception($"Payment failed for card {cardNumber}, CVV {cvv}: invalid amount");
        }
    }

    /// <summary>
    /// Log a transaction.
    /// BUG #2: Logs full credit card numbers and SSNs.
    /// FIX: Mask/redact sensitive data before logging.
    /// </summary>
    public void LogTransaction(string cardNumber, string ssn, decimal amount)
    {
        // ⚠️ VULNERABILITY: Logging sensitive data in full
        string logEntry = $"Transaction: card={cardNumber}, ssn={ssn}, amount={amount:C}";
        _logOutput.Add(logEntry);
    }

    /// <summary>
    /// Save customer data to a JSON file.
    /// BUG #4: Writes unencrypted passwords and SSNs to file.
    /// FIX: Encrypt sensitive fields or exclude them from the output.
    /// </summary>
    public string SaveCustomerData(Customer customer)
    {
        // ⚠️ VULNERABILITY: Sensitive data written to file unencrypted
        string json = JsonSerializer.Serialize(customer, new JsonSerializerOptions { WriteIndented = true });
        return json; // In real code this would be File.WriteAllText
    }

    /// <summary>
    /// Build an API URL.
    /// BUG #5: Puts API key and credentials in URL query parameters.
    /// FIX: Return a tuple of (url, headers) with credentials in headers.
    /// </summary>
    public (string Url, Dictionary<string, string> Headers) BuildApiUrl(string apiKey, string userId)
    {
        // ⚠️ VULNERABILITY: Credentials in URL query string
        string url = $"https://api.example.com/data?api_key={apiKey}&user_id={userId}";
        return (url, new Dictionary<string, string>());
    }

    /// <summary>
    /// Process sensitive input.
    /// BUG #6: Password stored in regular string, byte arrays never cleared.
    /// FIX: Zero out byte arrays after use with CryptographicOperations.ZeroMemory().
    /// </summary>
    public byte[] ProcessSensitiveInput(string password)
    {
        // ⚠️ VULNERABILITY: Sensitive data stays in memory
        byte[] passwordBytes = Encoding.UTF8.GetBytes(password);
        byte[] hash = SHA256.HashData(passwordBytes);
        // passwordBytes should be zeroed after use but isn't
        return hash;
    }

    /// <summary>
    /// Check if sensitive byte arrays are zeroed after use.
    /// The ProcessSensitiveInput method should zero its intermediate byte array.
    /// This is hard to test directly, so we test a flag.
    /// </summary>
    public bool WasSensitiveDataCleared { get; set; } = false;
}
