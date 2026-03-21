using System.Text.Json;

/// <summary>
/// Data parser with INTENTIONALLY VULNERABLE deserialization.
/// </summary>
public class DataParser
{
    /// <summary>
    /// BUG #4: No MaxDepth or input size limit on deserialization.
    /// FIX: Set MaxDepth = 32 and check input length before parsing.
    /// Throw ArgumentException if input exceeds 1MB or nesting is too deep.
    /// </summary>
    public T? ParseResponse<T>(string json)
    {
        // ⚠️ VULNERABILITY: Unbounded deserialization
        return JsonSerializer.Deserialize<T>(json);
    }
}
