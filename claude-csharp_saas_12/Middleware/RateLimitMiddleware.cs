using System.Collections.Concurrent;

namespace TeamTrackr.Middleware;

public class RateLimitMiddleware
{
    private readonly RequestDelegate _next;
    private static readonly ConcurrentDictionary<string, RateLimitEntry> _clients = new();
    private const int ApiKeyRequestsPerMinute = 100;
    private const int JwtRequestsPerMinute = 30;

    public RateLimitMiddleware(RequestDelegate next)
    {
        _next = next;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        var clientKey = GetClientKey(context);
        if (clientKey == null)
        {
            await _next(context);
            return;
        }

        var limit = context.User?.FindFirst("auth_type")?.Value == "apikey"
            ? ApiKeyRequestsPerMinute
            : JwtRequestsPerMinute;

        var entry = _clients.GetOrAdd(clientKey, _ => new RateLimitEntry());

        lock (entry)
        {
            var now = DateTime.UtcNow;
            if (now - entry.WindowStart > TimeSpan.FromMinutes(1))
            {
                entry.WindowStart = now;
                entry.RequestCount = 0;
            }

            entry.RequestCount++;

            if (entry.RequestCount > limit)
            {
                context.Response.StatusCode = StatusCodes.Status429TooManyRequests;
                context.Response.Headers["Retry-After"] = "60";
                return;
            }
        }

        await _next(context);
    }

    private static string? GetClientKey(HttpContext context)
    {
        var apiKeyId = context.User?.FindFirst("api_key_id")?.Value;
        if (apiKeyId != null) return $"apikey:{apiKeyId}";

        var userId = context.User?.FindFirst("sub")?.Value
            ?? context.User?.FindFirst(System.Security.Claims.ClaimTypes.NameIdentifier)?.Value;
        if (userId != null) return $"jwt:{userId}";

        return null;
    }

    private class RateLimitEntry
    {
        public DateTime WindowStart { get; set; } = DateTime.UtcNow;
        public int RequestCount { get; set; }
    }
}
