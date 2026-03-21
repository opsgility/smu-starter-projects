/// <summary>
/// File upload handling with INTENTIONALLY VULNERABLE code.
/// </summary>
public class UploadHandler
{
    public const int MaxFileSize = 10 * 1024 * 1024; // 10 MB

    /// <summary>
    /// BUG #3: Validates file type by extension only — no magic bytes check.
    /// FIX: Check the file signature (magic bytes) at the start of the byte array.
    /// JPEG starts with: 0xFF 0xD8 0xFF
    /// </summary>
    public bool ValidateUpload(string filename, byte[] fileBytes)
    {
        // ⚠️ VULNERABILITY: Extension-only validation
        return Path.GetExtension(filename).ToLower() == ".jpg";
    }

    /// <summary>
    /// BUG #5: No file size limit — accepts any size.
    /// FIX: Check fileBytes.Length against MaxFileSize before processing.
    /// Throw ArgumentException if too large.
    /// </summary>
    public string ProcessUpload(byte[] fileBytes)
    {
        // ⚠️ VULNERABILITY: No size limit
        // Should check: if (fileBytes.Length > MaxFileSize) throw new ArgumentException(...)
        return $"Processed {fileBytes.Length} bytes";
    }
}
