using TeamTrackr.Models;

namespace TeamTrackr.Services;

public interface IBillingService
{
    Task<string> CreateCheckoutSessionAsync(int tenantId, SubscriptionPlan plan);
    Task HandleWebhookAsync(string payload);
    Task<Subscription?> GetSubscriptionAsync(int tenantId);
    Task<bool> CancelSubscriptionAsync(int tenantId);
    PlanLimits GetPlanLimits(SubscriptionPlan plan);
}
