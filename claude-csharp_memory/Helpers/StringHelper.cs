namespace MemoryApp.Helpers;

// Mix of sync and async methods (inconsistent)
public static class StringHelper
{
    public static string Capitalize(string input)
    {
        if (string.IsNullOrEmpty(input)) return input;
        return char.ToUpper(input[0]) + input[1..];
    }

    public static string Truncate(string input, int maxLength)
    {
        if (input.Length <= maxLength) return input;
        return input[..maxLength] + "...";
    }

    // Async method doing I/O mixed with sync methods
    public static async Task<string> ReadFromFileAsync(string path)
    {
        return await File.ReadAllTextAsync(path);
    }
}
