namespace PaymentApp;

public class Payment
{
    public decimal Amount { get; set; }
    public string CardNumber { get; set; } = string.Empty;
    public string ExpiryDate { get; set; } = string.Empty;
    public string CVV { get; set; } = string.Empty;
    public string PaymentMethod { get; set; } = "credit";
    public string ItemCategory { get; set; } = "standard";
}
