using PaymentApp;

var processor = new PaymentProcessor();

var payment = new Payment
{
    Amount = 100.00m,
    CardNumber = "4111111111111111",
    ExpiryDate = "12/27",
    CVV = "123",
    PaymentMethod = "credit",
    ItemCategory = "standard"
};

Console.WriteLine("=== Processing Payment ===");
var result = processor.ProcessPayment(payment);
Console.WriteLine($"\nResult: {result.Success} - {result.Message}");
Console.WriteLine($"Transaction ID: {result.TransactionId}");
