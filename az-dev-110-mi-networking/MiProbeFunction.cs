using Azure.Core;
using Azure.Security.KeyVault.Secrets;
using Azure.Storage.Blobs;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.Logging;

namespace Anchorline.Functions.MiNetworking;

public class MiProbeFunction
{
    private readonly BlobServiceClient _blobs;
    private readonly SecretClient _kv;
    private readonly TokenCredential _credential;
    private readonly ILogger<MiProbeFunction> _log;

    public MiProbeFunction(BlobServiceClient blobs, SecretClient kv, TokenCredential credential, ILogger<MiProbeFunction> log)
    {
        _blobs = blobs;
        _kv = kv;
        _credential = credential;
        _log = log;
    }

    [Function("Whoami")]
    public async Task<IActionResult> Whoami([HttpTrigger(AuthorizationLevel.Function, "get", Route = "whoami")] HttpRequest req)
    {
        try
        {
            var token = await _credential.GetTokenAsync(
                new TokenRequestContext(new[] { "https://management.azure.com/.default" }),
                CancellationToken.None);
            var parts = token.Token.Split('.');
            var payload = System.Text.Encoding.UTF8.GetString(
                Convert.FromBase64String(PadBase64(parts[1])));
            return new OkObjectResult(new { tokenPayload = System.Text.Json.JsonDocument.Parse(payload).RootElement, expiresOn = token.ExpiresOn });
        }
        catch (Exception ex)
        {
            return new ObjectResult(new { error = ex.Message }) { StatusCode = 500 };
        }

        static string PadBase64(string s) => s.PadRight(s.Length + (4 - s.Length % 4) % 4, '=').Replace('-', '+').Replace('_', '/');
    }

    [Function("ListBlobs")]
    public async Task<IActionResult> ListBlobs([HttpTrigger(AuthorizationLevel.Function, "get", Route = "blobs")] HttpRequest req)
    {
        try
        {
            var container = _blobs.GetBlobContainerClient("anchorline-uploads");
            await container.CreateIfNotExistsAsync();
            var names = new List<string>();
            await foreach (var blob in container.GetBlobsAsync())
            {
                names.Add(blob.Name);
                if (names.Count >= 20) break;
            }
            return new OkObjectResult(new { container = "anchorline-uploads", count = names.Count, names });
        }
        catch (Exception ex)
        {
            _log.LogError(ex, "ListBlobs failed");
            return new ObjectResult(new { error = ex.Message }) { StatusCode = 500 };
        }
    }

    [Function("GetSecret")]
    public async Task<IActionResult> GetSecret(
        [HttpTrigger(AuthorizationLevel.Function, "get", Route = "secret/{name}")] HttpRequest req,
        string name)
    {
        try
        {
            var secret = await _kv.GetSecretAsync(name);
            var v = secret.Value.Value;
            var masked = v.Length > 8 ? v.Substring(0, 4) + "..." + v.Substring(v.Length - 4) : "****";
            return new OkObjectResult(new { name, valueMasked = masked });
        }
        catch (Exception ex)
        {
            _log.LogError(ex, "GetSecret failed");
            return new ObjectResult(new { error = ex.Message }) { StatusCode = 500 };
        }
    }
}
