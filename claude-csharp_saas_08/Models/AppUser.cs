using Microsoft.AspNetCore.Identity;

namespace TeamTrackr.Models;

public class AppUser : IdentityUser
{
    public int TenantId { get; set; }
    public Tenant Tenant { get; set; } = null!;
    public string DisplayName { get; set; } = string.Empty;
    public UserRole Role { get; set; } = UserRole.Member;
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
}
