namespace TeamTrackr.Models;

public enum InvitationStatus { Pending, Accepted, Revoked, Expired }

public class TenantInvitation
{
    public int Id { get; set; }
    public int TenantId { get; set; }
    public Tenant Tenant { get; set; } = null!;
    public string Email { get; set; } = string.Empty;
    public string Token { get; set; } = string.Empty;
    public UserRole Role { get; set; } = UserRole.Member;
    public InvitationStatus Status { get; set; } = InvitationStatus.Pending;
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public DateTime ExpiresAt { get; set; }
    public string InvitedByUserId { get; set; } = string.Empty;
    public AppUser InvitedBy { get; set; } = null!;
}
