using System.Diagnostics;

namespace TeamTrackr.Middleware;

public class RequestLoggingMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<RequestLoggingMiddleware> _logger;

    public RequestLoggingMiddleware(RequestDelegate next, ILogger<RequestLoggingMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        var stopwatch = Stopwatch.StartNew();

        try
        {
            await _next(context);
        }
        finally
        {
            stopwatch.Stop();

            var tenantId = context.Items.TryGetValue("TenantId", out var tid) ? tid?.ToString() : "none";
            var userId = context.User?.FindFirst("sub")?.Value
                ?? context.User?.FindFirst(System.Security.Claims.ClaimTypes.NameIdentifier)?.Value
                ?? "anonymous";

            _logger.LogInformation(
                "HTTP {Method} {Path} responded {StatusCode} in {Duration}ms | Tenant: {TenantId} | User: {UserId}",
                context.Request.Method,
                context.Request.Path,
                context.Response.StatusCode,
                stopwatch.ElapsedMilliseconds,
                tenantId,
                userId);
        }
    }
}
