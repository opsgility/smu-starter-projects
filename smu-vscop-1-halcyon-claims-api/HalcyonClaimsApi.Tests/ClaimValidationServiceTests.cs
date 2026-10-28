using HalcyonClaimsApi.Models;
using HalcyonClaimsApi.Services;
using Xunit;

namespace HalcyonClaimsApi.Tests;

public class ClaimValidationServiceTests
{
    private static Policy ActivePolicy() => new()
    {
        Id = 1,
        PolicyNumber = "POL-0000001",
        Holder = "Jordan Avery",
        CoverageAmount = 100_000m,
        EffectiveDate = DateTime.UtcNow.AddMonths(-6),
        ExpirationDate = DateTime.UtcNow.AddMonths(6),
        IsActive = true
    };

    [Fact]
    public async Task ValidateClaimAsync_HappyPath_ReturnsValid()
    {
        var sut = new ClaimValidationService();
        var claim = new Claim { PolicyNumber = "POL-0000001", ClaimAmount = 500m, IncidentDate = DateTime.UtcNow.AddDays(-1), Description = "Test" };

        var (isValid, reason) = await sut.ValidateClaimAsync(claim, ActivePolicy());

        Assert.True(isValid);
        Assert.Equal("Claim is valid.", reason);
    }

    [Fact]
    public async Task ValidateClaimAsync_NullPolicy_ReturnsInvalid()
    {
        var sut = new ClaimValidationService();
        var claim = new Claim { PolicyNumber = "POL-0000001", ClaimAmount = 500m, IncidentDate = DateTime.UtcNow };

        var (isValid, _) = await sut.ValidateClaimAsync(claim, null);

        Assert.False(isValid);
    }

    [Fact]
    public async Task ValidateClaimAsync_AmountExceedsCoverage_ReturnsInvalid()
    {
        var sut = new ClaimValidationService();
        var policy = ActivePolicy();
        var claim = new Claim { PolicyNumber = "POL-0000001", ClaimAmount = policy.CoverageAmount + 1m, IncidentDate = DateTime.UtcNow };

        var (isValid, reason) = await sut.ValidateClaimAsync(claim, policy);

        Assert.False(isValid);
        Assert.Contains("exceeds", reason);
    }
}
