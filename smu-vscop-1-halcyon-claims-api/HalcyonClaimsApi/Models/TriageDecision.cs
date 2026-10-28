namespace HalcyonClaimsApi.Models;

public enum TriageOutcome
{
    AutoApprove,
    Review,
    Deny
}

public class TriageDecision
{
    public TriageOutcome Outcome { get; set; }
    public string Reason { get; set; } = string.Empty;
}
