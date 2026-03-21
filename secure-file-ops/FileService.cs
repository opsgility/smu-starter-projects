/// <summary>
/// File operations with INTENTIONALLY VULNERABLE code.
/// </summary>
public class FileService
{
    /// <summary>
    /// BUG #1: Path traversal in read — no validation of filename containing ..
    /// FIX: Use Path.GetFileName() and verify resolved path starts with baseDir.
    /// </summary>
    public string ReadUserFile(string baseDir, string filename)
    {
        // ⚠️ VULNERABILITY: Path traversal
        string path = Path.Combine(baseDir, filename);
        return File.ReadAllText(path);
    }

    /// <summary>
    /// BUG #2: Path traversal in write — same issue as ReadUserFile.
    /// FIX: Canonicalize and validate path.
    /// </summary>
    public void SaveUserFile(string baseDir, string filename, string data)
    {
        // ⚠️ VULNERABILITY: Path traversal in write
        string path = Path.Combine(baseDir, filename);
        File.WriteAllText(path, data);
    }

    /// <summary>
    /// BUG #4: Predictable temp file name — attacker can pre-create/symlink.
    /// FIX: Use Path.GetRandomFileName() or Path.GetTempFileName().
    /// </summary>
    public string CreateTempReport(string content)
    {
        // ⚠️ VULNERABILITY: Predictable filename
        string path = Path.Combine(Path.GetTempPath(), "report.txt");
        File.WriteAllText(path, content);
        return path;
    }

    /// <summary>
    /// Returns just the filename portion for testing path traversal prevention.
    /// </summary>
    public string GetSafeFilename(string input)
    {
        // This should strip directory components
        return input; // BUG: returns raw input
    }

    /// <summary>
    /// BUG #6: TOCTOU — checks File.Exists() then File.Delete() separately.
    /// FIX: Just try to delete and catch FileNotFoundException.
    /// </summary>
    public bool SafeDeleteFile(string path)
    {
        // ⚠️ VULNERABILITY: Time-of-check vs time-of-use
        if (File.Exists(path))
        {
            File.Delete(path);
            return true;
        }
        return false;
    }
}
