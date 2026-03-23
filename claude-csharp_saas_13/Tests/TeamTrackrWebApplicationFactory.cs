using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.IdentityModel.Tokens;
using TeamTrackr.Auth;
using TeamTrackr.Data;
using TeamTrackr.Models;

namespace TeamTrackr.Tests;

public class TeamTrackrWebApplicationFactory : WebApplicationFactory<Program>
{
    private readonly string _dbName = Guid.NewGuid().ToString();

    // Seeded test data references
    public int TestTenantId { get; private set; } = 1;
    public string TestUserId { get; private set; } = string.Empty;
    public string TestUserEmail => "testuser@acme.com";
    public string TestUserPassword => "TestPass1234";

    public int TenantBId { get; private set; }
    public string TenantBUserId { get; private set; } = string.Empty;
    public string TenantBUserEmail => "user@otherco.com";
    public string TenantBUserPassword => "TestPass1234";

    private const string JwtKey = "TeamTrackrSuperSecretKeyThatIsLongEnoughForHmacSha256!";
    private const string JwtIssuer = "TeamTrackr";
    private const string JwtAudience = "TeamTrackrUsers";

    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.ConfigureServices(services =>
        {
            // Remove existing DbContext registration
            var descriptor = services.SingleOrDefault(
                d => d.ServiceType == typeof(DbContextOptions<AppDbContext>));
            if (descriptor != null) services.Remove(descriptor);

            // Remove the ITenantProvider so we can re-register it
            var tenantProviderDescriptor = services.SingleOrDefault(
                d => d.ServiceType == typeof(ITenantProvider));
            if (tenantProviderDescriptor != null) services.Remove(tenantProviderDescriptor);

            // Add InMemory database
            services.AddDbContext<AppDbContext>((sp, options) =>
            {
                options.UseInMemoryDatabase(_dbName);
            });

            // Re-register the TenantProvider (needs HttpContextAccessor)
            services.AddScoped<ITenantProvider, TenantProvider>();

            // Build a temporary service provider to seed the database
            var sp = services.BuildServiceProvider();
            using var scope = sp.CreateScope();
            var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
            var userManager = scope.ServiceProvider.GetRequiredService<UserManager<AppUser>>();

            db.Database.EnsureCreated();
            SeedData(db, userManager).GetAwaiter().GetResult();
        });

        builder.UseEnvironment("Development");
    }

    private async Task SeedData(AppDbContext db, UserManager<AppUser> userManager)
    {
        // The default tenant (Id=1) is seeded by OnModelCreating HasData
        // Ensure it exists in InMemory (HasData works for InMemory)
        var tenantA = await db.Tenants.FindAsync(1);
        if (tenantA == null)
        {
            tenantA = new Tenant
            {
                Id = 1,
                Name = "Default Organization",
                Slug = "default",
                Plan = "free",
                CreatedAt = new DateTime(2025, 1, 1, 0, 0, 0, DateTimeKind.Utc)
            };
            db.Tenants.Add(tenantA);
            await db.SaveChangesAsync();
        }
        TestTenantId = tenantA.Id;

        // Seed test user in Tenant A
        var userA = new AppUser
        {
            UserName = TestUserEmail,
            Email = TestUserEmail,
            DisplayName = "Test User",
            TenantId = TestTenantId,
            Role = UserRole.Owner
        };
        var result = await userManager.CreateAsync(userA, TestUserPassword);
        if (result.Succeeded)
        {
            TestUserId = userA.Id;
        }

        // Seed Tenant B for isolation tests
        var tenantB = new Tenant
        {
            Name = "Other Company",
            Slug = "otherco",
            Plan = "free",
            CreatedAt = DateTime.UtcNow
        };
        db.Tenants.Add(tenantB);
        await db.SaveChangesAsync();
        TenantBId = tenantB.Id;

        // Seed user in Tenant B
        var userB = new AppUser
        {
            UserName = TenantBUserEmail,
            Email = TenantBUserEmail,
            DisplayName = "Other User",
            TenantId = TenantBId,
            Role = UserRole.Owner
        };
        var resultB = await userManager.CreateAsync(userB, TenantBUserPassword);
        if (resultB.Succeeded)
        {
            TenantBUserId = userB.Id;
        }
    }

    /// <summary>
    /// Creates an HttpClient with a valid JWT for the specified tenant and user.
    /// </summary>
    public HttpClient CreateAuthenticatedClient(int tenantId, string userId, string email, string role = "Owner")
    {
        var client = CreateClient();
        var token = GenerateTestJwt(tenantId, userId, email, role);
        client.DefaultRequestHeaders.Authorization =
            new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", token);
        return client;
    }

    /// <summary>
    /// Creates an HttpClient authenticated as the default test user (Tenant A).
    /// </summary>
    public HttpClient CreateAuthenticatedClient()
    {
        return CreateAuthenticatedClient(TestTenantId, TestUserId, TestUserEmail);
    }

    /// <summary>
    /// Creates an HttpClient authenticated as Tenant B's user.
    /// </summary>
    public HttpClient CreateTenantBClient()
    {
        return CreateAuthenticatedClient(TenantBId, TenantBUserId, TenantBUserEmail);
    }

    private string GenerateTestJwt(int tenantId, string userId, string email, string role)
    {
        var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(JwtKey));
        var credentials = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

        var claims = new[]
        {
            new Claim(JwtRegisteredClaimNames.Sub, userId),
            new Claim(JwtRegisteredClaimNames.Email, email),
            new Claim("tenant_id", tenantId.ToString()),
            new Claim("role", role),
            new Claim(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString())
        };

        var token = new JwtSecurityToken(
            issuer: JwtIssuer,
            audience: JwtAudience,
            claims: claims,
            expires: DateTime.UtcNow.AddHours(1),
            signingCredentials: credentials);

        return new JwtSecurityTokenHandler().WriteToken(token);
    }
}
