using System.Security.Claims;
using System.Text.Encodings.Web;
using Microsoft.AspNetCore.Authentication;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Options;
using TeamTrackr.Data;

namespace TeamTrackr.Auth;

public static class ApiKeyAuthDefaults
{
    public const string AuthenticationScheme = "ApiKey";
}

public class ApiKeyAuthOptions : AuthenticationSchemeOptions
{
}

public class ApiKeyAuthHandler : AuthenticationHandler<ApiKeyAuthOptions>
{
    private readonly IServiceScopeFactory _scopeFactory;

    public ApiKeyAuthHandler(
        IOptionsMonitor<ApiKeyAuthOptions> options,
        ILoggerFactory logger,
        UrlEncoder encoder,
        IServiceScopeFactory scopeFactory)
        : base(options, logger, encoder)
    {
        _scopeFactory = scopeFactory;
    }

    protected override async Task<AuthenticateResult> HandleAuthenticateAsync()
    {
        if (!Request.Headers.TryGetValue("X-API-Key", out var apiKeyHeader))
        {
            return AuthenticateResult.NoResult();
        }

        var apiKeyValue = apiKeyHeader.ToString();
        if (string.IsNullOrEmpty(apiKeyValue))
        {
            return AuthenticateResult.Fail("API key is empty.");
        }

        using var scope = _scopeFactory.CreateScope();
        var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();

        var apiKey = await db.ApiKeys
            .IgnoreQueryFilters()
            .FirstOrDefaultAsync(k => k.Key == apiKeyValue && k.IsActive);

        if (apiKey == null)
        {
            return AuthenticateResult.Fail("Invalid API key.");
        }

        // Update last used timestamp
        apiKey.LastUsedAt = DateTime.UtcNow;
        await db.SaveChangesAsync();

        var claims = new[]
        {
            new Claim("tenant_id", apiKey.TenantId.ToString()),
            new Claim("api_key_id", apiKey.Id.ToString()),
            new Claim("auth_type", "apikey")
        };

        var identity = new ClaimsIdentity(claims, ApiKeyAuthDefaults.AuthenticationScheme);
        var principal = new ClaimsPrincipal(identity);
        var ticket = new AuthenticationTicket(principal, ApiKeyAuthDefaults.AuthenticationScheme);

        return AuthenticateResult.Success(ticket);
    }
}
