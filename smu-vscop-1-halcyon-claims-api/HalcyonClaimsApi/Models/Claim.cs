namespace HalcyonClaimsApi.Models;

public class Claim
{
    public int Id { get; set; }
    public string PolicyNumber { get; set; } = string.Empty;
    public decimal ClaimAmount { get; set; }
    public DateTime IncidentDate { get; set; }
    public string Description { get; set; } = string.Empty;
    public string Status { get; set; } = "Submitted";
}
