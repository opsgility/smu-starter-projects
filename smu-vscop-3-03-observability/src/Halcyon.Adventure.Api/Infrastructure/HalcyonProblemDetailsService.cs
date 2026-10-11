using System.Diagnostics;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Http.HttpResults;
using Microsoft.AspNetCore.Mvc;

namespace Halcyon.Adventure.Api.Infrastructure;

/// <summary>
/// Custom IProblemDetailsService wiring. Every validation failure, 4xx, and
/// unhandled 5xx leaves the API with:
///   - "traceId"  — matches the W3C trace parent so support can grep logs.
///   - "halcyonCorrelationId" — mirrors the X-Correlation-Id header (introduced
///     in Lesson 6; falls back to Activity.Current.Id until the middleware lands).
///   - "type"      — Halcyon's problem-type registry URL rather than RFC links.
/// </summary>
public sealed class HalcyonProblemDetailsService : IProblemDetailsService
{
    private const string HalcyonProblemTypeBase =
        "https://halcyon.example.com/problems";

    private readonly IHttpContextAccessor _httpContextAccessor;

    public HalcyonProblemDetailsService(IHttpContextAccessor httpContextAccessor)
    {
        _httpContextAccessor = httpContextAccessor;
    }

    public ValueTask WriteAsync(ProblemDetailsContext context)
    {
        var http = context.HttpContext;
        var problem = context.ProblemDetails;

        problem.Extensions["traceId"] = Activity.Current?.Id ?? http.TraceIdentifier;

        if (http.Request.Headers.TryGetValue("X-Correlation-Id", out var correlationId) &&
            !string.IsNullOrWhiteSpace(correlationId))
        {
            problem.Extensions["halcyonCorrelationId"] = correlationId.ToString();
        }

        if (problem.Status is int status)
        {
            problem.Type ??= $"{HalcyonProblemTypeBase}/{status}";
        }

        http.Response.StatusCode = problem.Status ?? StatusCodes.Status500InternalServerError;
        http.Response.ContentType = "application/problem+json";

        return new ValueTask(http.Response.WriteAsJsonAsync(problem,
            options: null,
            contentType: "application/problem+json"));
    }

    public ValueTask<bool> TryWriteAsync(ProblemDetailsContext context)
    {
        // The default writer handles Accept-header negotiation; delegate to it,
        // then stamp our extensions on the way out.
        var http = context.HttpContext;
        var accept = http.Request.Headers.Accept.ToString();
        var acceptsProblem = string.IsNullOrEmpty(accept) ||
            accept.Contains("application/json", StringComparison.OrdinalIgnoreCase) ||
            accept.Contains("application/problem+json", StringComparison.OrdinalIgnoreCase) ||
            accept.Contains("*/*", StringComparison.Ordinal);

        if (!acceptsProblem)
        {
            return new ValueTask<bool>(false);
        }

        return new ValueTask<bool>(WriteAndReturnTrue(context));
    }

    private async Task<bool> WriteAndReturnTrue(ProblemDetailsContext context)
    {
        await WriteAsync(context);
        return true;
    }
}
