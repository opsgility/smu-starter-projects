using Xunit;
using PaymentApp;

namespace PaymentApp.Tests;

public class PaymentProcessorTests
{
    private readonly PaymentProcessor _processor = new();

    [Fact]
    public void ProcessPayment_ValidCreditCard_ReturnsSuccess()
    {
        var payment = new Payment
        {
            Amount = 50.00m, CardNumber = "4111111111111111",
            ExpiryDate = "12/27", CVV = "123",
            PaymentMethod = "credit", ItemCategory = "standard"
        };
        var result = _processor.ProcessPayment(payment);
        Assert.True(result.Success);
        Assert.NotEmpty(result.TransactionId);
    }

    [Fact]
    public void ProcessPayment_ShortCardNumber_ReturnsFailure()
    {
        var payment = new Payment
        {
            Amount = 50.00m, CardNumber = "411",
            ExpiryDate = "12/27", CVV = "123"
        };
        var result = _processor.ProcessPayment(payment);
        Assert.False(result.Success);
        Assert.Contains("Invalid card number", result.Message);
    }

    [Fact]
    public void ProcessPayment_ExpiredCard_ReturnsFailure()
    {
        var payment = new Payment
        {
            Amount = 50.00m, CardNumber = "4111111111111111",
            ExpiryDate = "01/20", CVV = "123"
        };
        var result = _processor.ProcessPayment(payment);
        Assert.False(result.Success);
        Assert.Contains("expired", result.Message);
    }
}
