namespace PaymentApp;

public class PaymentProcessor
{
    public PaymentResult ProcessPayment(Payment payment)
    {
        // VALIDATION - all in one method (SRP violation)
        if (string.IsNullOrEmpty(payment.CardNumber) || payment.CardNumber.Length < 13 || payment.CardNumber.Length > 19)
        {
            Console.WriteLine($"[LOG] Payment validation failed: invalid card number length ({payment.CardNumber?.Length ?? 0})");
            return new PaymentResult { Success = false, Message = "Invalid card number. Must be 13-19 digits." };
        }

        if (string.IsNullOrEmpty(payment.ExpiryDate) || payment.ExpiryDate.Length != 5 || payment.ExpiryDate[2] != '/')
        {
            Console.WriteLine("[LOG] Payment validation failed: invalid expiry format");
            return new PaymentResult { Success = false, Message = "Invalid expiry date format. Use MM/YY." };
        }

        var parts = payment.ExpiryDate.Split('/');
        var month = int.Parse(parts[0]);
        var year = int.Parse(parts[1]) + 2000;
        var expiryDate = new DateTime(year, month, 1).AddMonths(1).AddDays(-1);
        if (expiryDate < DateTime.Now)
        {
            Console.WriteLine($"[LOG] Payment validation failed: card expired ({payment.ExpiryDate})");
            return new PaymentResult { Success = false, Message = "Card has expired." };
        }

        if (string.IsNullOrEmpty(payment.CVV) || payment.CVV.Length < 3 || payment.CVV.Length > 4)
        {
            Console.WriteLine("[LOG] Payment validation failed: invalid CVV");
            return new PaymentResult { Success = false, Message = "Invalid CVV. Must be 3-4 digits." };
        }

        // CALCULATE FEE - switch statement (OCP violation)
        decimal fee;
        switch (payment.PaymentMethod.ToLower())
        {
            case "credit":
                fee = payment.Amount * 0.025m;
                Console.WriteLine($"[LOG] Credit card fee: {fee:C}");
                break;
            case "debit":
                fee = payment.Amount * 0.015m;
                Console.WriteLine($"[LOG] Debit card fee: {fee:C}");
                break;
            case "paypal":
                fee = payment.Amount * 0.03m;
                Console.WriteLine($"[LOG] PayPal fee: {fee:C}");
                break;
            default:
                Console.WriteLine($"[LOG] Unknown payment method: {payment.PaymentMethod}");
                return new PaymentResult { Success = false, Message = $"Unsupported payment method: {payment.PaymentMethod}" };
        }

        // CALCULATE TAX - magic numbers
        decimal taxRate;
        switch (payment.ItemCategory.ToLower())
        {
            case "standard":
                taxRate = 0.08m;
                break;
            case "food":
                taxRate = 0.05m;
                break;
            case "medicine":
                taxRate = 0.0m;
                break;
            default:
                taxRate = 0.08m;
                break;
        }
        var tax = payment.Amount * taxRate;
        var totalAmount = payment.Amount + fee + tax;

        Console.WriteLine($"[LOG] Tax ({taxRate:P0}): {tax:C}");
        Console.WriteLine($"[LOG] Total charged: {totalAmount:C}");

        // PROCESS - simulate processing
        var transactionId = Guid.NewGuid().ToString("N")[..12].ToUpper();
        Console.WriteLine($"[LOG] Processing payment of {totalAmount:C} via {payment.PaymentMethod}...");
        Console.WriteLine($"[LOG] Transaction {transactionId} completed successfully");

        // NOTIFICATION - hardcoded (DIP violation)
        Console.WriteLine($"[NOTIFICATION] Payment of {totalAmount:C} processed successfully. Transaction ID: {transactionId}");
        Console.WriteLine($"[EMAIL] Sending receipt to customer for transaction {transactionId}");

        return new PaymentResult
        {
            Success = true,
            Message = $"Payment of {totalAmount:C} processed successfully via {payment.PaymentMethod}",
            TransactionId = transactionId
        };
    }
}
