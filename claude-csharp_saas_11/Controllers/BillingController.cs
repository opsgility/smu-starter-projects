using System.Security.Claims;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using TeamTrackr.Auth;
using TeamTrackr.Models;
using TeamTrackr.Services;

namespace TeamTrackr.Controllers;

[ApiController]
[Route("api/[controller]")]
[Authorize]
public class BillingController : ControllerBase
{
    private readonly IBillingService _billingService;
    private readonly ITenantProvider _tenantProvider;

    public BillingController(IBillingService billingService, ITenantProvider tenantProvider)
    {
        _billingService = billingService;
        _tenantProvider = tenantProvider;
    }

    /// <summary>
    /// Get the current subscription for the tenant.
    /// </summary>
    [HttpGet("subscription")]
    public async Task<IActionResult> GetSubscription()
    {
        var tenantId = _tenantProvider.GetCurrentTenantId();
        if (tenantId == 0) return Unauthorized();

        var subscription = await _billingService.GetSubscriptionAsync(tenantId);
        if (subscription == null) return NotFound();

        return Ok(new
        {
            subscription.Id,
            subscription.TenantId,
            Plan = subscription.Plan.ToString(),
            Status = subscription.Status.ToString(),
            subscription.CurrentPeriodStart,
            subscription.CurrentPeriodEnd,
            Limits = _billingService.GetPlanLimits(subscription.Plan)
        });
    }

    /// <summary>
    /// Create a checkout session (simulated Stripe).
    /// </summary>
    [HttpPost("checkout")]
    public async Task<IActionResult> CreateCheckoutSession([FromBody] CheckoutRequest request)
    {
        var tenantId = _tenantProvider.GetCurrentTenantId();
        if (tenantId == 0) return Unauthorized();

        if (!Enum.TryParse<SubscriptionPlan>(request.Plan, true, out var plan))
        {
            return BadRequest(new { error = "Invalid plan. Use Free, Pro, or Enterprise." });
        }

        var checkoutUrl = await _billingService.CreateCheckoutSessionAsync(tenantId, plan);
        return Ok(new { checkoutUrl, message = "Simulated checkout session created. Subscription has been activated." });
    }

    /// <summary>
    /// Handle a Stripe webhook (simulated). Allows anonymous access.
    /// </summary>
    [HttpPost("webhook")]
    [AllowAnonymous]
    public async Task<IActionResult> HandleWebhook()
    {
        using var reader = new StreamReader(Request.Body);
        var payload = await reader.ReadToEndAsync();

        await _billingService.HandleWebhookAsync(payload);
        return Ok(new { received = true });
    }

    /// <summary>
    /// Cancel the current subscription.
    /// </summary>
    [HttpPost("cancel")]
    public async Task<IActionResult> CancelSubscription()
    {
        var tenantId = _tenantProvider.GetCurrentTenantId();
        if (tenantId == 0) return Unauthorized();

        var cancelled = await _billingService.CancelSubscriptionAsync(tenantId);
        if (!cancelled) return NotFound(new { error = "No active subscription found." });

        return Ok(new { message = "Subscription cancelled. You have been downgraded to the Free plan." });
    }
}

public class CheckoutRequest
{
    public string Plan { get; set; } = string.Empty;
}
