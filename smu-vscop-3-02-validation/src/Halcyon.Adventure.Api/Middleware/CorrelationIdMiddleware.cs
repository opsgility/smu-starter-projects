namespace Halcyon.Adventure.Api.Middleware;

// Reads the X-Correlation-Id request header (mints a GUID if absent), pushes the
// value onto HttpContext.Items["HalcyonCorrelationId"] + an ILogger scope so every
// log line on this request carries it, and echoes it on the response as
// X-Correlation-Id via Response.OnStarting (headers lock once the response body
// starts).
//
// Lesson 4 Exercise 4 wires the custom problem-details delegate that reads
// HttpContext.Items["HalcyonCorrelationId"] and copies it onto every problem-details
// response as the halcyonTraceId extension.
public sealed class CorrelationIdMiddleware
{
    public const string HeaderName = "X-Correlation-Id";
    public const string ItemKey = "HalcyonCorrelationId";

    private readonly RequestDelegate _next;
    private readonly ILogger<CorrelationIdMiddleware> _logger;

    public CorrelationIdMiddleware(RequestDelegate next, ILogger<CorrelationIdMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        var incoming = context.Request.Headers[HeaderName].ToString();
        var correlationId = string.IsNullOrWhiteSpace(incoming) ? Guid.NewGuid().ToString() : incoming;

        context.Items[ItemKey] = correlationId;

        context.Response.OnStarting(() =>
        {
            context.Response.Headers[HeaderName] = correlationId;
            return Task.CompletedTask;
        });

        using (_logger.BeginScope(new Dictionary<string, object>
        {
            ["CorrelationId"] = correlationId,
        }))
        {
            await _next(context);
        }
    }
}
