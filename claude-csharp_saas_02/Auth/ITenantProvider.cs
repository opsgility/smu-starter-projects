namespace TeamTrackr.Auth;

public interface ITenantProvider
{
    int GetCurrentTenantId();
}
