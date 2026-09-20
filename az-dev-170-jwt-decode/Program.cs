using System.IdentityModel.Tokens.Jwt;
using Azure.Core;
using Azure.Identity;
using Microsoft.IdentityModel.Protocols;
using Microsoft.IdentityModel.Protocols.OpenIdConnect;
using Microsoft.IdentityModel.Tokens;

var tenantId = Environment.GetEnvironmentVariable("TENANT_ID") ?? throw new InvalidOperationException("TENANT_ID");
var scope = Environment.GetEnvironmentVariable("SCOPE") ?? "https://graph.microsoft.com/.default";

var cred = new AzureCliCredential();
var token = await cred.GetTokenAsync(new TokenRequestContext(new[] { scope }));

Console.WriteLine("Access token acquired (JWT):");
Console.WriteLine(token.Token);
Console.WriteLine();

var handler = new JwtSecurityTokenHandler();
var jwt = handler.ReadJwtToken(token.Token);
Console.WriteLine($"Header alg: {jwt.Header.Alg}");
Console.WriteLine($"Header kid: {jwt.Header.Kid}");
Console.WriteLine($"Payload aud: {jwt.Payload.Aud.FirstOrDefault()}");
Console.WriteLine($"Payload iss: {jwt.Payload.Iss}");
Console.WriteLine($"Payload sub: {jwt.Payload.Sub}");
Console.WriteLine($"Payload scp: {jwt.Payload["scp"]?.ToString() ?? "<none>"}");
Console.WriteLine($"Payload roles: {jwt.Payload["roles"]?.ToString() ?? "<none>"}");
Console.WriteLine($"Payload exp: {DateTimeOffset.FromUnixTimeSeconds(jwt.Payload.Exp!.Value):u}");

// Verify signature against tenant OIDC metadata
var mgr = new ConfigurationManager<OpenIdConnectConfiguration>(
    $"https://login.microsoftonline.com/{tenantId}/v2.0/.well-known/openid-configuration",
    new OpenIdConnectConfigurationRetriever());
var cfg = await mgr.GetConfigurationAsync(CancellationToken.None);

var parms = new TokenValidationParameters
{
    ValidateIssuer = true,
    ValidIssuer = cfg.Issuer,
    ValidateAudience = false,
    IssuerSigningKeys = cfg.SigningKeys,
    ValidateLifetime = true
};
try
{
    handler.ValidateToken(token.Token, parms, out _);
    Console.WriteLine("Signature: VALID");
}
catch (Exception ex)
{
    Console.WriteLine($"Signature: INVALID -- {ex.Message}");
}
