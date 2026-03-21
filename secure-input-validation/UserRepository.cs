using Microsoft.Data.Sqlite;
using System.Diagnostics;

/// <summary>
/// User repository with database operations.
/// SECURITY CHALLENGE: This file contains multiple security vulnerabilities.
/// Find and fix them all!
/// </summary>
public class UserRepository
{
    private readonly SqliteConnection _connection;

    public UserRepository(SqliteConnection connection)
    {
        _connection = connection;
    }

    /// <summary>
    /// Authenticate a user by username and password.
    /// BUG: Vulnerable to SQL injection — uses string concatenation.
    /// FIX: Use parameterized queries.
    /// </summary>
    public string? Authenticate(string username, string password)
    {
        // ⚠️ VULNERABILITY: SQL Injection via string concatenation
        var cmd = _connection.CreateCommand();
        cmd.CommandText = $"SELECT name FROM users WHERE username='{username}' AND password='{password}'";

        using var reader = cmd.ExecuteReader();
        if (reader.Read())
        {
            return reader.GetString(0);
        }
        return null;
    }

    /// <summary>
    /// Search users by name.
    /// BUG: Vulnerable to SQL injection in LIKE clause.
    /// FIX: Use parameterized LIKE queries.
    /// </summary>
    public List<string> SearchUsers(string searchTerm)
    {
        // ⚠️ VULNERABILITY: SQL Injection in LIKE clause
        var cmd = _connection.CreateCommand();
        cmd.CommandText = $"SELECT name FROM users WHERE name LIKE '%{searchTerm}%'";

        var results = new List<string>();
        using var reader = cmd.ExecuteReader();
        while (reader.Read())
        {
            results.Add(reader.GetString(0));
        }
        return results;
    }

    /// <summary>
    /// Create a new user.
    /// BUG: No input length validation — accepts any length username.
    /// FIX: Validate that username is between 3 and 50 characters.
    /// </summary>
    public void CreateUser(string username, string password, string name, string email)
    {
        // ⚠️ VULNERABILITY: No input length validation
        var cmd = _connection.CreateCommand();
        cmd.CommandText = "INSERT INTO users (username, password, name, email) VALUES (@u, @p, @n, @e)";
        cmd.Parameters.AddWithValue("@u", username);
        cmd.Parameters.AddWithValue("@p", password);
        cmd.Parameters.AddWithValue("@n", name);
        cmd.Parameters.AddWithValue("@e", email);
        cmd.ExecuteNonQuery();
    }

    /// <summary>
    /// Format a user profile as HTML.
    /// BUG: No HTML encoding — vulnerable to XSS.
    /// FIX: Use System.Net.WebUtility.HtmlEncode() on user-supplied values.
    /// </summary>
    public string FormatUserProfile(string name, string email)
    {
        // ⚠️ VULNERABILITY: No HTML encoding (XSS)
        return $"<div class='profile'><h2>{name}</h2><p>Email: {email}</p></div>";
    }

    /// <summary>
    /// Export user data to a file.
    /// BUG: No path validation — vulnerable to path traversal.
    /// FIX: Use Path.GetFileName() to strip directory components and validate.
    /// </summary>
    public void ExportUserData(string filename, string data)
    {
        // ⚠️ VULNERABILITY: Path traversal — no sanitization of filename
        string exportDir = Path.Combine(Path.GetTempPath(), "exports");
        Directory.CreateDirectory(exportDir);
        string fullPath = Path.Combine(exportDir, filename);
        File.WriteAllText(fullPath, data);
    }
}
