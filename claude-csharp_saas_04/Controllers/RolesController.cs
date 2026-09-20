using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using TeamTrackr.Auth;
using TeamTrackr.Models;

namespace TeamTrackr.Controllers;

[ApiController]
[Route("api/[controller]")]
[Authorize]
public class RolesController : ControllerBase
{
    private readonly UserManager<AppUser> _userManager;
    private readonly ITenantProvider _tenantProvider;

    public RolesController(UserManager<AppUser> userManager, ITenantProvider tenantProvider)
    {
        _userManager = userManager;
        _tenantProvider = tenantProvider;
    }

    /// <summary>Lists all users in the current tenant with their roles.</summary>
    [HttpGet]
    public IActionResult GetTenantUsers()
    {
        var tenantId = _tenantProvider.GetCurrentTenantId();
        var users = _userManager.Users
            .Where(u => u.TenantId == tenantId)
            .Select(u => new
            {
                u.Id,
                u.Email,
                u.DisplayName,
                Role = u.Role.ToString()
            })
            .ToList();

        return Ok(users);
    }

    /// <summary>Assigns a new role to a user within the current tenant. Requires Admin or Owner.</summary>
    [HttpPut("{userId}")]
    [Authorize(Policy = "RequireAdmin")]
    public async Task<IActionResult> AssignRole(string userId, [FromBody] AssignRoleRequest request)
    {
        var tenantId = _tenantProvider.GetCurrentTenantId();
        var currentUserId = User.FindFirst(System.Security.Claims.ClaimTypes.NameIdentifier)?.Value;

        var user = await _userManager.FindByIdAsync(userId);
        if (user == null || user.TenantId != tenantId)
            return NotFound(new { error = "User not found in this tenant." });

        // Prevent changing your own role
        if (user.Id == currentUserId)
            return BadRequest(new { error = "You cannot change your own role." });

        // Only Owners can assign Owner role or change Admin roles
        var callerRole = User.FindFirst("role")?.Value;
        if (request.Role == UserRole.Owner && callerRole != "Owner")
            return Forbid();

        if (user.Role == UserRole.Owner && callerRole != "Owner")
            return Forbid();

        // Remove old role and assign new one
        var oldRoles = await _userManager.GetRolesAsync(user);
        await _userManager.RemoveFromRolesAsync(user, oldRoles);
        await _userManager.AddToRoleAsync(user, request.Role.ToString());

        user.Role = request.Role;
        await _userManager.UpdateAsync(user);

        return Ok(new { message = $"Role updated to {request.Role}.", userId, role = request.Role.ToString() });
    }

    /// <summary>Removes a user from the tenant. Requires Owner role.</summary>
    [HttpDelete("{userId}")]
    [Authorize(Policy = "RequireOwner")]
    public async Task<IActionResult> RemoveUser(string userId)
    {
        var tenantId = _tenantProvider.GetCurrentTenantId();
        var currentUserId = User.FindFirst(System.Security.Claims.ClaimTypes.NameIdentifier)?.Value;

        var user = await _userManager.FindByIdAsync(userId);
        if (user == null || user.TenantId != tenantId)
            return NotFound(new { error = "User not found in this tenant." });

        if (user.Id == currentUserId)
            return BadRequest(new { error = "You cannot remove yourself from the tenant." });

        await _userManager.DeleteAsync(user);
        return NoContent();
    }
}

public class AssignRoleRequest
{
    public UserRole Role { get; set; }
}
