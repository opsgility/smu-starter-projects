using System.Net;
using System.Net.Http.Json;
using System.Text;
using System.Text.Json;
using TeamTrackr.DTOs;
using Xunit;

namespace TeamTrackr.Tests;

public class BillingTests : IClassFixture<TeamTrackrWebApplicationFactory>
{
    private readonly TeamTrackrWebApplicationFactory _factory;

    public BillingTests(TeamTrackrWebApplicationFactory factory)
    {
        _factory = factory;
    }

    /// <summary>
    /// Helper: register a brand new user+tenant so each test is isolated for billing state.
    /// Returns an authenticated HttpClient for that user.
    /// </summary>
    private async Task<HttpClient> CreateFreshTenantClient()
    {
        var anonymousClient = _factory.CreateClient();
        var slug = $"bill-{Guid.NewGuid():N}"[..20];
        var email = $"{slug}@test.com";

        var regReq = new RegisterRequest
        {
            Email = email,
            Password = "TestPass1234",
            DisplayName = "Billing User",
            TenantName = "Billing Org",
            TenantSlug = slug
        };

        var regResp = await anonymousClient.PostAsJsonAsync("/api/auth/register", regReq);
        regResp.EnsureSuccessStatusCode();
        var auth = await regResp.Content.ReadFromJsonAsync<AuthResponse>();

        var client = _factory.CreateClient();
        client.DefaultRequestHeaders.Authorization =
            new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", auth!.Token);
        return client;
    }

    [Fact]
    public async Task FreePlan_LimitsProjectCreation()
    {
        var client = await CreateFreshTenantClient();

        // Free plan allows 3 projects
        for (int i = 0; i < 3; i++)
        {
            var key = $"FP{i}{Guid.NewGuid():N}"[..6].ToUpper();
            var resp = await client.PostAsJsonAsync("/api/projects", new CreateProjectRequest
            {
                Name = $"Free Project {i}",
                Description = "Test",
                Key = key
            });
            Assert.True(resp.StatusCode == HttpStatusCode.Created,
                $"Project {i} creation failed with {resp.StatusCode}");
        }

        // 4th project should be blocked by PlanLimitMiddleware
        var key4 = $"FP4{Guid.NewGuid():N}"[..6].ToUpper();
        var blocked = await client.PostAsJsonAsync("/api/projects", new CreateProjectRequest
        {
            Name = "Over Limit Project",
            Description = "Should fail",
            Key = key4
        });
        Assert.Equal(HttpStatusCode.Forbidden, blocked.StatusCode);
    }

    [Fact]
    public async Task UpgradeToPro_AllowsMoreProjects()
    {
        var client = await CreateFreshTenantClient();

        // Create 3 projects (free limit)
        for (int i = 0; i < 3; i++)
        {
            var key = $"UP{i}{Guid.NewGuid():N}"[..6].ToUpper();
            await client.PostAsJsonAsync("/api/projects", new CreateProjectRequest
            {
                Name = $"Pre-Upgrade Project {i}",
                Description = "Test",
                Key = key
            });
        }

        // Upgrade to Pro
        var checkoutResp = await client.PostAsJsonAsync("/api/billing/checkout",
            new { Plan = "Pro" });
        Assert.Equal(HttpStatusCode.OK, checkoutResp.StatusCode);

        // Now should be able to create more
        var key4 = $"UP4{Guid.NewGuid():N}"[..6].ToUpper();
        var resp = await client.PostAsJsonAsync("/api/projects", new CreateProjectRequest
        {
            Name = "Post-Upgrade Project",
            Description = "Should succeed",
            Key = key4
        });
        Assert.Equal(HttpStatusCode.Created, resp.StatusCode);
    }

    [Fact]
    public async Task GetSubscription_ReturnsCurrentPlan()
    {
        var client = await CreateFreshTenantClient();

        var response = await client.GetAsync("/api/billing/subscription");

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        var json = await response.Content.ReadFromJsonAsync<JsonElement>();
        Assert.Equal("Free", json.GetProperty("plan").GetString());
        Assert.Equal("Active", json.GetProperty("status").GetString());
    }

    [Fact]
    public async Task Webhook_UpdatesSubscriptionStatus()
    {
        var client = await CreateFreshTenantClient();

        // First get the subscription to find the tenant ID
        var subResp = await client.GetAsync("/api/billing/subscription");
        var subJson = await subResp.Content.ReadFromJsonAsync<JsonElement>();
        var tenantId = subJson.GetProperty("tenantId").GetInt32();

        // Send a webhook to mark payment as failed
        var webhookPayload = JsonSerializer.Serialize(new
        {
            type = "invoice.payment_failed",
            tenant_id = tenantId
        });

        var anonymousClient = _factory.CreateClient();
        var webhookResp = await anonymousClient.PostAsync("/api/billing/webhook",
            new StringContent(webhookPayload, Encoding.UTF8, "application/json"));
        Assert.Equal(HttpStatusCode.OK, webhookResp.StatusCode);

        // Verify the subscription status changed
        var checkResp = await client.GetAsync("/api/billing/subscription");
        var checkJson = await checkResp.Content.ReadFromJsonAsync<JsonElement>();
        Assert.Equal("PastDue", checkJson.GetProperty("status").GetString());
    }

    [Fact]
    public async Task CancelSubscription_RevertsToFree()
    {
        var client = await CreateFreshTenantClient();

        // Upgrade to Pro first
        await client.PostAsJsonAsync("/api/billing/checkout", new { Plan = "Pro" });

        // Verify it's Pro
        var subResp = await client.GetAsync("/api/billing/subscription");
        var subJson = await subResp.Content.ReadFromJsonAsync<JsonElement>();
        Assert.Equal("Pro", subJson.GetProperty("plan").GetString());

        // Cancel
        var cancelResp = await client.PostAsync("/api/billing/cancel", null);
        Assert.Equal(HttpStatusCode.OK, cancelResp.StatusCode);

        // Verify reverted — the subscription record shows Cancelled status
        var checkResp = await client.GetAsync("/api/billing/subscription");
        var checkJson = await checkResp.Content.ReadFromJsonAsync<JsonElement>();
        Assert.Equal("Cancelled", checkJson.GetProperty("status").GetString());
    }
}
