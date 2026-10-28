using HalcyonClaimsApi.Models;

namespace HalcyonClaimsApi.Services;

public interface IClaimValidationService
{
    Task<(bool IsValid, string Reason)> ValidateClaimAsync(Claim claim, Policy? policy);
}

public class ClaimValidationService : IClaimValidationService
{
    private readonly List<Claim> _recentClaims = new();

    public Task<(bool IsValid, string Reason)> ValidateClaimAsync(Claim claim, Policy? policy)
    {
        if (claim is null)
        {
            return Task.FromResult((false, "Claim is null."));
        }

        if (policy is null)
        {
            return Task.FromResult((false, "Policy not found for the provided policy number."));
        }

        if (!policy.IsActive)
        {
            return Task.FromResult((false, "Policy is not active."));
        }

        var now = DateTime.UtcNow;
        if (now < policy.EffectiveDate || now > policy.ExpirationDate)
        {
            return Task.FromResult((false, "Policy is outside its effective date range."));
        }

        if (claim.ClaimAmount <= 0)
        {
            return Task.FromResult((false, "Claim amount must be greater than zero."));
        }

        if (claim.ClaimAmount > policy.CoverageAmount)
        {
            return Task.FromResult((false, "Claim amount exceeds the policy coverage amount."));
        }

        var duplicate = _recentClaims.Any(c =>
            c.PolicyNumber == claim.PolicyNumber &&
            c.ClaimAmount == claim.ClaimAmount &&
            c.IncidentDate.Date == claim.IncidentDate.Date);

        if (duplicate)
        {
            return Task.FromResult((false, "Duplicate claim detected for this policy and incident date."));
        }

        _recentClaims.Add(claim);
        return Task.FromResult((true, "Claim is valid."));
    }
}
