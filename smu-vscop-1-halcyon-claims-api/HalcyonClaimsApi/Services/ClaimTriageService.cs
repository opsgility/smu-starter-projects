using HalcyonClaimsApi.Models;

namespace HalcyonClaimsApi.Services;

public interface IClaimTriageService
{
    TriageDecision Triage(Claim claim, Policy policy, IReadOnlyList<Claim> recentClaimsForPolicy);
}

public class ClaimTriageService : IClaimTriageService
{
    private const decimal SmallClaimThreshold = 1000m;
    private const decimal AutoApproveCoverageRatio = 0.10m;
    private const decimal ReviewCoverageRatio = 0.50m;
    private const int FraudWatchDaysFromEffective = 2;
    private const int FraudWatchClaimCountWithin30Days = 3;

    public TriageDecision Triage(Claim claim, Policy policy, IReadOnlyList<Claim> recentClaimsForPolicy)
    {
        var claimToCoverageRatio = policy.CoverageAmount <= 0
            ? 1m
            : claim.ClaimAmount / policy.CoverageAmount;

        var withinFraudWatchWindow =
            (claim.IncidentDate - policy.EffectiveDate).TotalDays <= FraudWatchDaysFromEffective;

        var recentClaimCount = recentClaimsForPolicy.Count(c =>
            (claim.IncidentDate - c.IncidentDate).TotalDays <= 30);

        if (withinFraudWatchWindow || recentClaimCount >= FraudWatchClaimCountWithin30Days)
        {
            return new TriageDecision
            {
                Outcome = TriageOutcome.Review,
                Reason = "fraud-watch: claim submitted close to policy effective date or frequent recent claims."
            };
        }

        if (claim.ClaimAmount < SmallClaimThreshold)
        {
            return new TriageDecision
            {
                Outcome = TriageOutcome.AutoApprove,
                Reason = $"Claim amount under ${SmallClaimThreshold:N0} threshold."
            };
        }

        if (claimToCoverageRatio < AutoApproveCoverageRatio)
        {
            return new TriageDecision
            {
                Outcome = TriageOutcome.AutoApprove,
                Reason = "Claim is a small share of total coverage."
            };
        }

        if (claimToCoverageRatio < ReviewCoverageRatio)
        {
            return new TriageDecision
            {
                Outcome = TriageOutcome.Review,
                Reason = "Claim is between 10% and 50% of coverage; manual review required."
            };
        }

        return new TriageDecision
        {
            Outcome = TriageOutcome.Review,
            Reason = "Claim is a large share of coverage; senior adjuster review required."
        };
    }
}
