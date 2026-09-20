using TeamTrackr.DTOs;

namespace TeamTrackr.Services;

public interface IInvitationService
{
    Task<InviteResponse> InviteAsync(InviteRequest request, string invitedByUserId, int tenantId);
    Task<AuthResponse> AcceptAsync(AcceptInvitationRequest request);
    Task<List<PendingInvitationResponse>> GetPendingAsync(int tenantId);
    Task RevokeAsync(int invitationId, int tenantId);
}
