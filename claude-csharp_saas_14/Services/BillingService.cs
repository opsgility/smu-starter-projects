using System.Text.Json;
using Microsoft.EntityFrameworkCore;
using TeamTrackr.Data;
using TeamTrackr.Models;

namespace TeamTrackr.Services;

public class BillingService : IBillingService
{
    private readonly AppDbContext _db;

    public BillingService(AppDbContext db)
    {
        _db = db;
    }

    public async Task<string> CreateCheckoutSessionAsync(int tenantId, SubscriptionPlan plan)
    {
        // Simulate Stripe checkout session creation
        var subscription = await _db.Subscriptions
            .FirstOrDefaultAsync(s => s.TenantId == tenantId);

        if (subscription == null)
        {
            subscription = new Subscription
            {
                TenantId = tenantId,
                Plan = plan,
                Status = SubscriptionStatus.Active,
                CurrentPeriodStart = DateTime.UtcNow,
                CurrentPeriodEnd = DateTime.UtcNow.AddMonths(1),
                StripeSubscriptionId = $"sub_simulated_{Guid.NewGuid():N}",
                StripeCustomerId = $"cus_simulated_{tenantId}"
            };
            _db.Subscriptions.Add(subscription);
        }
        else
        {
            subscription.Plan = plan;
            subscription.Status = SubscriptionStatus.Active;
            subscription.CurrentPeriodStart = DateTime.UtcNow;
            subscription.CurrentPeriodEnd = DateTime.UtcNow.AddMonths(1);
            subscription.UpdatedAt = DateTime.UtcNow;
        }

        // Update the tenant's plan field to match
        var tenant = await _db.Tenants.FindAsync(tenantId);
        if (tenant != null)
        {
            tenant.Plan = plan.ToString().ToLower();
        }

        await _db.SaveChangesAsync();

        // Return a simulated checkout URL
        var sessionId = Guid.NewGuid().ToString("N");
        return $"https://checkout.stripe.com/simulated/session/{sessionId}";
    }

    public async Task HandleWebhookAsync(string payload)
    {
        // Simulate processing a Stripe webhook event
        // In production, you'd verify the signature and parse the event type
        try
        {
            using var doc = JsonDocument.Parse(payload);
            var root = doc.RootElement;

            var eventType = root.GetProperty("type").GetString();
            var tenantId = root.GetProperty("tenant_id").GetInt32();

            var subscription = await _db.Subscriptions
                .FirstOrDefaultAsync(s => s.TenantId == tenantId);

            if (subscription == null) return;

            switch (eventType)
            {
                case "invoice.payment_succeeded":
                    subscription.Status = SubscriptionStatus.Active;
                    subscription.CurrentPeriodEnd = DateTime.UtcNow.AddMonths(1);
                    break;

                case "invoice.payment_failed":
                    subscription.Status = SubscriptionStatus.PastDue;
                    break;

                case "customer.subscription.deleted":
                    subscription.Status = SubscriptionStatus.Cancelled;
                    break;
            }

            subscription.UpdatedAt = DateTime.UtcNow;
            await _db.SaveChangesAsync();
        }
        catch (JsonException)
        {
            // Invalid payload — ignore in simulation
        }
    }

    public async Task<Subscription?> GetSubscriptionAsync(int tenantId)
    {
        var subscription = await _db.Subscriptions
            .FirstOrDefaultAsync(s => s.TenantId == tenantId);

        // If no subscription exists, return a default free subscription
        if (subscription == null)
        {
            subscription = new Subscription
            {
                TenantId = tenantId,
                Plan = SubscriptionPlan.Free,
                Status = SubscriptionStatus.Active,
                CurrentPeriodStart = DateTime.UtcNow,
                CurrentPeriodEnd = DateTime.UtcNow.AddMonths(1)
            };
            _db.Subscriptions.Add(subscription);
            await _db.SaveChangesAsync();
        }

        return subscription;
    }

    public async Task<bool> CancelSubscriptionAsync(int tenantId)
    {
        var subscription = await _db.Subscriptions
            .FirstOrDefaultAsync(s => s.TenantId == tenantId);

        if (subscription == null) return false;

        subscription.Status = SubscriptionStatus.Cancelled;
        subscription.UpdatedAt = DateTime.UtcNow;

        // Revert tenant plan to free
        var tenant = await _db.Tenants.FindAsync(tenantId);
        if (tenant != null)
        {
            tenant.Plan = "free";
        }

        await _db.SaveChangesAsync();
        return true;
    }

    public PlanLimits GetPlanLimits(SubscriptionPlan plan)
    {
        return plan switch
        {
            SubscriptionPlan.Pro => PlanLimits.Pro(),
            SubscriptionPlan.Enterprise => PlanLimits.Enterprise(),
            _ => PlanLimits.Free()
        };
    }
}
