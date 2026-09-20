namespace TeamTrackr.Auth;

public class TenantProvider : ITenantProvider
{
    private readonly IHttpContextAccessor _httpContextAccessor;

    public TenantProvider(IHttpContextAccessor httpContextAccessor)
    {
        _httpContextAccessor = httpContextAccessor;
    }

    public int GetCurrentTenantId()
    {
        var context = _httpContextAccessor.HttpContext;
        if (context?.Items.TryGetValue("TenantId", out var tenantIdObj) == true
            && tenantIdObj is int tenantId)
        {
            return tenantId;
        }

        // Try from claims as fallback
        var claim = context?.User?.FindFirst("tenant_id");
        if (claim != null && int.TryParse(claim.Value, out var claimTenantId))
        {
            return claimTenantId;
        }

        return 0;
    }
}
