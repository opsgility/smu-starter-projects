/// <summary>
/// Database client with INTENTIONALLY VULNERABLE secrets management.
/// </summary>
public class DatabaseClient
{
    private readonly List<string> _logOutput = new();
    public IReadOnlyList<string> LogOutput => _logOutput;

    /// <summary>
    /// Get the database connection string.
    /// BUG #1: Hardcoded connection string with real credentials.
    /// FIX: Read from IConfiguration or Environment.GetEnvironmentVariable("DB_CONNECTION_STRING").
    /// </summary>
    public string GetConnectionString()
    {
        // ⚠️ VULNERABILITY: Hardcoded connection string with credentials
        return "Server=prod-db.internal;Database=myapp;User=admin;Password=P@ssw0rd123!;";
    }

    /// <summary>
    /// Connect to the database.
    /// BUG #4: Logs the full connection string including password.
    /// FIX: Remove the log line or redact the password.
    /// </summary>
    public string Connect()
    {
        string connectionString = GetConnectionString();

        // ⚠️ VULNERABILITY: Logging connection string with password
        string logEntry = $"Connecting with: {connectionString}";
        _logOutput.Add(logEntry);

        return "Connected"; // Simulated
    }
}
