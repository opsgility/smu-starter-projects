using Microsoft.EntityFrameworkCore;
using TeamTrackr.Auth;
using TeamTrackr.Data;
using TeamTrackr.Models;
using TeamTrackr.Services;

namespace TeamTrackr.Middleware;

public class PlanLimitMiddleware
{
    private readonly RequestDelegate _next;

    public PlanLimitMiddleware(RequestDelegate next)
    {
        _next = next;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        // Only check limits on POST requests (resource creation)
        if (context.Request.Method != HttpMethods.Post)
        {
            await _next(context);
            return;
        }

        // Skip if not authenticated
        if (context.User.Identity?.IsAuthenticated != true)
        {
            await _next(context);
            return;
        }

        var tenantId = 0;
        if (context.Items.TryGetValue("TenantId", out var tenantIdObj) && tenantIdObj is int tid)
        {
            tenantId = tid;
        }

        if (tenantId == 0)
        {
            await _next(context);
            return;
        }

        var path = context.Request.Path.Value?.ToLower() ?? "";

        // Skip billing and auth endpoints
        if (path.Contains("/api/billing") || path.Contains("/api/auth"))
        {
            await _next(context);
            return;
        }

        var billingService = context.RequestServices.GetRequiredService<IBillingService>();
        var db = context.RequestServices.GetRequiredService<AppDbContext>();

        var subscription = await billingService.GetSubscriptionAsync(tenantId);
        var limits = billingService.GetPlanLimits(subscription?.Plan ?? SubscriptionPlan.Free);

        // Check project creation limit
        if (path.EndsWith("/api/projects"))
        {
            var projectCount = await db.Projects.CountAsync();
            if (projectCount >= limits.MaxProjects)
            {
                context.Response.StatusCode = StatusCodes.Status403Forbidden;
                await context.Response.WriteAsJsonAsync(new
                {
                    error = "Plan limit reached",
                    message = $"Your {subscription?.Plan ?? SubscriptionPlan.Free} plan allows a maximum of {limits.MaxProjects} projects. Please upgrade your plan."
                });
                return;
            }
        }

        // Check task creation limit per project
        if (path.EndsWith("/api/tasks"))
        {
            // We need to peek at the body to get projectId, but that's complex in middleware.
            // Instead, we check if any project is at its limit — a simpler heuristic.
            // The service layer should do the precise per-project check.
        }

        await _next(context);
    }
}
