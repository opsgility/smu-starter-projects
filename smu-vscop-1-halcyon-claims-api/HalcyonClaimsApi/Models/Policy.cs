namespace HalcyonClaimsApi.Models;

public class Policy
{
    public int Id { get; set; }
    public string PolicyNumber { get; set; } = string.Empty;
    public string Holder { get; set; } = string.Empty;
    public decimal CoverageAmount { get; set; }
    public DateTime EffectiveDate { get; set; }
    public DateTime ExpirationDate { get; set; }
    public bool IsActive { get; set; }
}
