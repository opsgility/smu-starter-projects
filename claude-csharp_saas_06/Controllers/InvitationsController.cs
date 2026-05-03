using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using TeamTrackr.Auth;
using TeamTrackr.DTOs;
using TeamTrackr.Services;

namespace TeamTrackr.Controllers;

[ApiController]
[Route("api/[controller]")]
public class InvitationsController : ControllerBase
{
    private readonly IInvitationService _invitationService;
    private readonly ITenantProvider _tenantProvider;

    public InvitationsController(IInvitationService invitationService, ITenantProvider tenantProvider)
    {
        _invitationService = invitationService;
        _tenantProvider = tenantProvider;
    }

    /// <summary>Invites a user to the current tenant by email. Requires Admin or Owner.</summary>
    [HttpPost]
    [Authorize(Policy = "RequireAdmin")]
    public async Task<IActionResult> Invite([FromBody] InviteRequest request)
    {
        var tenantId = _tenantProvider.GetCurrentTenantId();
        var userId = User.FindFirst(System.Security.Claims.ClaimTypes.NameIdentifier)?.Value!;

        try
        {
            var result = await _invitationService.InviteAsync(request, userId, tenantId);
            return Ok(result);
        }
        catch (InvalidOperationException ex)
        {
            return BadRequest(new { error = ex.Message });
        }
    }

    /// <summary>Lists pending invitations for the current tenant. Requires Admin or Owner.</summary>
    [HttpGet("pending")]
    [Authorize(Policy = "RequireAdmin")]
    public async Task<IActionResult> GetPending()
    {
        var tenantId = _tenantProvider.GetCurrentTenantId();
        var invitations = await _invitationService.GetPendingAsync(tenantId);
        return Ok(invitations);
    }

    /// <summary>Accepts an invitation and creates a new user account. No authentication required.</summary>
    [HttpPost("accept")]
    [AllowAnonymous]
    public async Task<IActionResult> Accept([FromBody] AcceptInvitationRequest request)
    {
        try
        {
            var result = await _invitationService.AcceptAsync(request);
            return Ok(result);
        }
        catch (InvalidOperationException ex)
        {
            return BadRequest(new { error = ex.Message });
        }
    }

    /// <summary>Revokes a pending invitation. Requires Admin or Owner.</summary>
    [HttpDelete("{id}")]
    [Authorize(Policy = "RequireAdmin")]
    public async Task<IActionResult> Revoke(int id)
    {
        var tenantId = _tenantProvider.GetCurrentTenantId();

        try
        {
            await _invitationService.RevokeAsync(id, tenantId);
            return NoContent();
        }
        catch (InvalidOperationException ex)
        {
            return NotFound(new { error = ex.Message });
        }
    }
}
