using System.Diagnostics;
using System.Text.RegularExpressions;

/// <summary>
/// Runs system commands.
/// SECURITY CHALLENGE: Contains a command injection vulnerability.
/// </summary>
public class CommandRunner
{
    /// <summary>
    /// Ping a hostname.
    /// BUG: Passes user input directly to a shell command — command injection.
    /// FIX: Validate hostname against a regex allowlist (alphanumeric, dots, hyphens only).
    ///       Throw ArgumentException if the hostname contains invalid characters.
    /// </summary>
    public string Ping(string hostname)
    {
        // ⚠️ VULNERABILITY: Command injection — user input passed directly to shell
        // An attacker could pass "127.0.0.1; rm -rf /" to execute arbitrary commands

        // TODO: Add hostname validation here. Only allow:
        //   - Letters (a-z, A-Z)
        //   - Numbers (0-9)
        //   - Dots (.) and hyphens (-)
        //   - Max length 253 characters
        // Throw ArgumentException for invalid hostnames.

        var psi = new ProcessStartInfo
        {
            FileName = "ping",
            Arguments = hostname,
            RedirectStandardOutput = true,
            UseShellExecute = false,
            CreateNoWindow = true
        };

        using var process = Process.Start(psi);
        if (process == null) return "Failed to start process";
        string output = process.StandardOutput.ReadToEnd();
        process.WaitForExit();
        return output;
    }
}
