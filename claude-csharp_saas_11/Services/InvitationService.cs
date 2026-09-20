using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using TeamTrackr.Auth;
using TeamTrackr.Data;
using TeamTrackr.DTOs;
using TeamTrackr.Models;

namespace TeamTrackr.Services;

public class InvitationService : IInvitationService
{
    private readonly AppDbContext _db;
    private readonly UserManager<AppUser> _userManager;
    private readonly IJwtTokenService _jwtTokenService;

    public InvitationService(
        AppDbContext db,
        UserManager<AppUser> userManager,
        IJwtTokenService jwtTokenService)
    {
        _db = db;
        _userManager = userManager;
        _jwtTokenService = jwtTokenService;
    }

    public async Task<InviteResponse> InviteAsync(InviteRequest request, string invitedByUserId, int tenantId)
    {
        // Revoke any existing pending invitation for this email in this tenant
        var existing = await _db.TenantInvitations
            .Where(i => i.TenantId == tenantId && i.Email == request.Email && i.Status == InvitationStatus.Pending)
            .FirstOrDefaultAsync();

        if (existing != null)
        {
            existing.Status = InvitationStatus.Revoked;
        }

        var invitation = new TenantInvitation
        {
            TenantId = tenantId,
            Email = request.Email,
            Token = Convert.ToBase64String(Guid.NewGuid().ToByteArray()).TrimEnd('=').Replace('+', '-').Replace('/', '_'),
            Role = request.Role,
            Status = InvitationStatus.Pending,
            InvitedByUserId = invitedByUserId,
            ExpiresAt = DateTime.UtcNow.AddDays(7)
        };

        _db.TenantInvitations.Add(invitation);
        await _db.SaveChangesAsync();

        return new InviteResponse
        {
            InvitationId = invitation.Id,
            Email = invitation.Email,
            Role = invitation.Role.ToString(),
            Token = invitation.Token,
            ExpiresAt = invitation.ExpiresAt
        };
    }

    public async Task<AuthResponse> AcceptAsync(AcceptInvitationRequest request)
    {
        var invitation = await _db.TenantInvitations
            .IgnoreQueryFilters()
            .Include(i => i.Tenant)
            .FirstOrDefaultAsync(i => i.Token == request.Token);

        if (invitation == null)
            throw new InvalidOperationException("Invitation not found.");

        if (invitation.Status != InvitationStatus.Pending)
            throw new InvalidOperationException($"Invitation is {invitation.Status}.");

        if (invitation.ExpiresAt < DateTime.UtcNow)
        {
            invitation.Status = InvitationStatus.Expired;
            await _db.SaveChangesAsync();
            throw new InvalidOperationException("Invitation has expired.");
        }

        var existingUser = await _userManager.FindByEmailAsync(invitation.Email);
        if (existingUser != null)
            throw new InvalidOperationException("An account with this email already exists.");

        var user = new AppUser
        {
            UserName = invitation.Email,
            Email = invitation.Email,
            DisplayName = request.DisplayName,
            TenantId = invitation.TenantId,
            Role = invitation.Role
        };

        var result = await _userManager.CreateAsync(user, request.Password);
        if (!result.Succeeded)
        {
            var errors = string.Join(", ", result.Errors.Select(e => e.Description));
            throw new InvalidOperationException($"Account creation failed: {errors}");
        }

        await _userManager.AddToRoleAsync(user, invitation.Role.ToString());

        invitation.Status = InvitationStatus.Accepted;
        await _db.SaveChangesAsync();

        var token = _jwtTokenService.GenerateAccessToken(user);
        var refreshToken = _jwtTokenService.GenerateRefreshToken();

        return new AuthResponse
        {
            Token = token,
            RefreshToken = refreshToken,
            UserId = user.Id,
            Email = user.Email!,
            DisplayName = user.DisplayName,
            Role = user.Role.ToString(),
            TenantId = invitation.TenantId,
            TenantName = invitation.Tenant.Name
        };
    }

    public async Task<List<PendingInvitationResponse>> GetPendingAsync(int tenantId)
    {
        var now = DateTime.UtcNow;

        // Expire overdue invitations
        var expired = await _db.TenantInvitations
            .Where(i => i.TenantId == tenantId && i.Status == InvitationStatus.Pending && i.ExpiresAt < now)
            .ToListAsync();

        foreach (var inv in expired)
            inv.Status = InvitationStatus.Expired;

        if (expired.Count > 0)
            await _db.SaveChangesAsync();

        return await _db.TenantInvitations
            .Where(i => i.TenantId == tenantId && i.Status == InvitationStatus.Pending)
            .Include(i => i.InvitedBy)
            .Select(i => new PendingInvitationResponse
            {
                Id = i.Id,
                Email = i.Email,
                Role = i.Role.ToString(),
                Status = i.Status.ToString(),
                ExpiresAt = i.ExpiresAt,
                InvitedByName = i.InvitedBy.DisplayName
            })
            .ToListAsync();
    }

    public async Task RevokeAsync(int invitationId, int tenantId)
    {
        var invitation = await _db.TenantInvitations
            .FirstOrDefaultAsync(i => i.Id == invitationId && i.TenantId == tenantId);

        if (invitation == null)
            throw new InvalidOperationException("Invitation not found.");

        if (invitation.Status != InvitationStatus.Pending)
            throw new InvalidOperationException("Only pending invitations can be revoked.");

        invitation.Status = InvitationStatus.Revoked;
        await _db.SaveChangesAsync();
    }
}
