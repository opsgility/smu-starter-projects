using Microsoft.Data.Sqlite;
using System.Net.Http.Headers;
using System.Security.Cryptography;
using System.Text;

/// <summary>
/// User Management Application with 10 INTENTIONALLY VULNERABLE security issues.
/// This capstone combines vulnerabilities from all 7 previous lessons.
/// Find and fix ALL 10 to pass the security audit.
/// </summary>
public class UserManagementApp
{
    private readonly SqliteConnection _db;
    private readonly List<string> _logOutput = new();

    /// <summary>BUG #7: Hardcoded API key (Lesson 6 - Secrets)</summary>
    public const string ApiKey = "sk-prod-realkey123secretvalue";

    public IReadOnlyList<string> LogOutput => _logOutput;

    public UserManagementApp(SqliteConnection db)
    {
        _db = db;
    }

    /// <summary>
    /// BUG #1: SQL injection via string concatenation (Lesson 1 - Injection).
    /// FIX: Use parameterized queries.
    /// </summary>
    public List<string> SearchUsers(string searchTerm)
    {
        var cmd = _db.CreateCommand();
        // ⚠️ SQL INJECTION
        cmd.CommandText = $"SELECT name FROM users WHERE name LIKE '%{searchTerm}%'";
        var results = new List<string>();
        using var reader = cmd.ExecuteReader();
        while (reader.Read()) results.Add(reader.GetString(0));
        return results;
    }

    /// <summary>
    /// BUG #2: Stores password in plaintext (Lesson 2 - Auth).
    /// FIX: Use BCrypt.Net.BCrypt.HashPassword().
    /// BUG #9: No input length validation on username (Lesson 1 - Input Validation).
    /// FIX: Validate username length (3-50 chars).
    /// </summary>
    public void RegisterUser(string username, string password, string name)
    {
        // ⚠️ NO INPUT VALIDATION (Bug #9)
        // ⚠️ PLAINTEXT PASSWORD (Bug #2)
        var cmd = _db.CreateCommand();
        cmd.CommandText = "INSERT INTO users (username, password, name) VALUES (@u, @p, @n)";
        cmd.Parameters.AddWithValue("@u", username);
        cmd.Parameters.AddWithValue("@p", password); // Plaintext!
        cmd.Parameters.AddWithValue("@n", name);
        cmd.ExecuteNonQuery();
    }

    /// <summary>
    /// BUG #3: Compares passwords with == (Lesson 2 - Auth).
    /// FIX: Use BCrypt.Net.BCrypt.Verify().
    /// </summary>
    public bool Login(string username, string password)
    {
        var cmd = _db.CreateCommand();
        cmd.CommandText = "SELECT password FROM users WHERE username = @u";
        cmd.Parameters.AddWithValue("@u", username);
        using var reader = cmd.ExecuteReader();
        if (reader.Read())
        {
            string storedPassword = reader.GetString(0);
            // ⚠️ PLAINTEXT COMPARISON (Bug #3)
            return storedPassword == password;
        }
        return false;
    }

    /// <summary>
    /// BUG #4: Uses AES-ECB mode (Lesson 3 - Crypto).
    /// FIX: Use CBC with random IV or AES-GCM.
    /// </summary>
    public byte[] EncryptUserData(string data, byte[] key)
    {
        using var aes = Aes.Create();
        aes.Key = key;
        // ⚠️ ECB MODE (Bug #4)
        aes.Mode = CipherMode.ECB;
        aes.IV = new byte[16];
        using var enc = aes.CreateEncryptor();
        byte[] plainBytes = Encoding.UTF8.GetBytes(data);
        return enc.TransformFinalBlock(plainBytes, 0, plainBytes.Length);
    }

    /// <summary>
    /// BUG #5: Logs passwords and tokens (Lesson 4 - Data Handling).
    /// FIX: Never log sensitive data. Redact or remove.
    /// </summary>
    public void LogActivity(string username, string password, string action)
    {
        // ⚠️ SENSITIVE DATA IN LOGS (Bug #5)
        string log = $"User={username}, Password={password}, Action={action}, Token={ApiKey}";
        _logOutput.Add(log);
    }

    /// <summary>
    /// BUG #6: Path traversal — unsanitized filename (Lesson 5 - Files).
    /// FIX: Use Path.GetFileName() and validate resolved path.
    /// </summary>
    public string ExportData(string filename, string data)
    {
        string exportDir = Path.Combine(Path.GetTempPath(), "capstone-exports");
        Directory.CreateDirectory(exportDir);
        // ⚠️ PATH TRAVERSAL (Bug #6)
        string fullPath = Path.Combine(exportDir, filename);
        File.WriteAllText(fullPath, data);
        return fullPath;
    }

    /// <summary>
    /// Get the API key.
    /// BUG #7 is the hardcoded const above.
    /// FIX: Read from Environment.GetEnvironmentVariable("API_KEY").
    /// </summary>
    public string GetApiKey() => ApiKey;

    /// <summary>
    /// BUG #8: Disabled SSL certificate validation (Lesson 7 - API).
    /// FIX: Remove the callback.
    /// </summary>
    public bool HasSslValidationDisabled()
    {
        // ⚠️ SSL VALIDATION DISABLED (Bug #8)
        // This simulates the pattern — in real code it would be on HttpClientHandler
        return true; // Indicates validation is disabled
    }

    /// <summary>
    /// Create an HttpClient. Returns whether SSL is properly configured.
    /// </summary>
    public HttpClient CreateHttpClient()
    {
        var handler = new HttpClientHandler();
        // ⚠️ Bug #8 in action:
        handler.ServerCertificateCustomValidationCallback = (_, _, _, _) => true;
        return new HttpClient(handler);
    }

    /// <summary>
    /// BUG #10: Credentials in URL query parameters (Lesson 6/7).
    /// FIX: Move credentials to Authorization header.
    /// </summary>
    public (string Url, Dictionary<string, string> Headers) BuildExternalUrl(string apiKey, string userId)
    {
        // ⚠️ CREDENTIALS IN URL (Bug #10)
        string url = $"https://external-api.com/data?api_key={apiKey}&user={userId}";
        return (url, new Dictionary<string, string>());
    }
}
