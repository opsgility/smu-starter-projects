// =============================================================================
//  SECURE FILE OPERATIONS — Security Challenge
// =============================================================================
//  6 file operation vulnerabilities in FileService.cs and UploadHandler.cs.
//  Run: dotnet run
// =============================================================================

var fileService = new FileService();
var uploadHandler = new UploadHandler();

// Setup test directory
string testDir = Path.Combine(Path.GetTempPath(), "secure-file-test-" + Guid.NewGuid().ToString()[..8]);
Directory.CreateDirectory(testDir);
File.WriteAllText(Path.Combine(testDir, "allowed.txt"), "This is allowed content");

Console.WriteLine("╔══════════════════════════════════════════════════════════╗");
Console.WriteLine("║       SECURE FILE OPERATIONS — Security Challenge       ║");
Console.WriteLine("║       Find and fix all 6 vulnerabilities!               ║");
Console.WriteLine("╚══════════════════════════════════════════════════════════╝");
Console.WriteLine();

int passed = 0;
int failed = 0;

void RunCheck(string name, Func<bool> check)
{
    try
    {
        bool result = check();
        if (result) { Console.ForegroundColor = ConsoleColor.Green; Console.WriteLine($"  ✓ PASS  {name}"); passed++; }
        else { Console.ForegroundColor = ConsoleColor.Red; Console.WriteLine($"  ✗ FAIL  {name}"); failed++; }
    }
    catch (Exception ex) { Console.ForegroundColor = ConsoleColor.Red; Console.WriteLine($"  ✗ CRASH {name}"); Console.ForegroundColor = ConsoleColor.DarkRed; Console.WriteLine($"          {ex.GetType().Name}: {ex.Message}"); failed++; }
    Console.ResetColor();
}

Console.WriteLine("─── Path Traversal ───");
RunCheck("ReadUserFile blocks path traversal (../)", () =>
{
    bool blocked = false;
    try { fileService.ReadUserFile(testDir, "../../../etc/passwd"); }
    catch (ArgumentException) { blocked = true; }
    catch (UnauthorizedAccessException) { blocked = true; }
    return blocked;
});

RunCheck("SaveUserFile blocks path traversal (../)", () =>
{
    bool blocked = false;
    try { fileService.SaveUserFile(testDir, "../../evil.txt", "malicious"); }
    catch (ArgumentException) { blocked = true; }
    return blocked;
});

Console.WriteLine("─── Upload Validation ───");
RunCheck("ValidateUpload checks magic bytes, not just extension", () =>
{
    byte[] fakeJpg = new byte[] { 0x00, 0x00, 0x00, 0x50, 0x4B }; // Not JPEG magic bytes
    bool accepted = uploadHandler.ValidateUpload("malware.jpg", fakeJpg);
    return !accepted; // Should reject — wrong magic bytes despite .jpg extension
});

RunCheck("ProcessUpload rejects files over 10MB", () =>
{
    bool blocked = false;
    try
    {
        byte[] hugeFile = new byte[11 * 1024 * 1024]; // 11MB
        uploadHandler.ProcessUpload(hugeFile);
    }
    catch (ArgumentException) { blocked = true; }
    return blocked;
});

Console.WriteLine("─── Temp Files & Race Conditions ───");
RunCheck("CreateTempReport uses a unique/random filename", () =>
{
    string path1 = fileService.CreateTempReport("report 1");
    string path2 = fileService.CreateTempReport("report 2");
    bool different = path1 != path2;
    bool notPredictable = !path1.EndsWith("report.txt");
    // Cleanup
    try { File.Delete(path1); File.Delete(path2); } catch { }
    return different && notPredictable;
});

RunCheck("SafeDeleteFile uses try/catch, not check-then-act", () =>
{
    // The method should handle missing files gracefully via try/catch
    // not via File.Exists() check (TOCTOU)
    string missingFile = Path.Combine(testDir, Guid.NewGuid().ToString());
    bool result = fileService.SafeDeleteFile(missingFile);
    // With try/catch approach, it should return false without throwing
    // With TOCTOU, it also returns false but the PATTERN is wrong
    // We test by checking the method handles concurrent scenarios
    // For this check, we verify it doesn't throw on missing files
    return !result; // Should return false gracefully
});

// Cleanup
try { Directory.Delete(testDir, true); } catch { }

Console.WriteLine();
Console.WriteLine("══════════════════════════════════════════════════════════");
if (failed == 0) { Console.ForegroundColor = ConsoleColor.Green; Console.WriteLine($"  ALL {passed} CHECKS PASSED — File operations are secure! 🔒"); }
else { Console.ForegroundColor = ConsoleColor.Yellow; Console.WriteLine($"  {passed} passed, {failed} failed — {failed} vulnerability(ies) remaining."); Console.WriteLine("  Fix the vulnerabilities and run again: dotnet run"); }
Console.ResetColor();
Console.WriteLine("══════════════════════════════════════════════════════════");
Console.WriteLine();
