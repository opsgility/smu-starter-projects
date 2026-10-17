namespace Halcyon.Adventure.Api.Middleware;

// Correlation-id middleware pre-staged by Marcus for the Lesson 5 observability
// sprint. Reads the X-Correlation-Id request header (mints a GUID if missing),
// pushes the value onto HttpContext.Items + an ILogger scope, and echoes it on
// the response via Response.OnStarting.
//
// Lesson 6 Exercise 2 opens with this file already in place — the student
// reviews the implementation with Copilot Agent mode and either accepts it as
// shipped or lands improvements before moving on.
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
        var correlationId = string.IsNullOrWhiteSpace(incoming)
            ? Guid.NewGuid().ToString()
            : incoming;

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

public static class CorrelationIdMiddlewareExtensions
{
    public static IApplicationBuilder UseCorrelationId(this IApplicationBuilder app) =>
        app.UseMiddleware<CorrelationIdMiddleware>();
}
