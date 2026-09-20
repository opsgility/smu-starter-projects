using System.Security.Claims;
using Microsoft.AspNetCore.Authorization;
using TaskFlow.Api.Models;

namespace TaskFlow.Api.Authorization;

public class TaskOwnerHandler : AuthorizationHandler<TaskOwnerRequirement, TaskItem>
{
    protected override Task HandleRequirementAsync(
        AuthorizationHandlerContext context,
        TaskOwnerRequirement requirement,
        TaskItem resource)
    {
        var userId = context.User.FindFirst(ClaimTypes.NameIdentifier)?.Value;

        if (userId == null)
            return Task.CompletedTask;

        // Admins can access any task
        if (context.User.IsInRole("Admin"))
        {
            context.Succeed(requirement);
            return Task.CompletedTask;
        }

        // Regular users can only access their own tasks
        if (resource.UserId == userId)
        {
            context.Succeed(requirement);
        }

        return Task.CompletedTask;
    }
}
