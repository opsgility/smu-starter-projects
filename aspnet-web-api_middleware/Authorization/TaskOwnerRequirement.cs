using Microsoft.AspNetCore.Authorization;

namespace TaskFlow.Api.Authorization;

public class TaskOwnerRequirement : IAuthorizationRequirement
{
}
