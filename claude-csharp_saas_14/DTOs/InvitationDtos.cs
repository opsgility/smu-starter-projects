using TeamTrackr.Models;

namespace TeamTrackr.DTOs;

public class InviteRequest
{
    public string Email { get; set; } = string.Empty;
    public UserRole Role { get; set; } = UserRole.Member;
}

public class InviteResponse
{
    public int InvitationId { get; set; }
    public string Email { get; set; } = string.Empty;
    public string Role { get; set; } = string.Empty;
    public string Token { get; set; } = string.Empty;
    public DateTime ExpiresAt { get; set; }
}

public class AcceptInvitationRequest
{
    public string Token { get; set; } = string.Empty;
    public string DisplayName { get; set; } = string.Empty;
    public string Password { get; set; } = string.Empty;
}

public class PendingInvitationResponse
{
    public int Id { get; set; }
    public string Email { get; set; } = string.Empty;
    public string Role { get; set; } = string.Empty;
    public string Status { get; set; } = string.Empty;
    public DateTime ExpiresAt { get; set; }
    public string InvitedByName { get; set; } = string.Empty;
}
