namespace MemoryApp.Models;

/// <summary>
/// Represents a customer order.
/// </summary>
public class Order
{
    /// <summary>Gets or sets the order identifier.</summary>
    public int Id { get; set; }

    /// <summary>Gets or sets the order date.</summary>
    public DateTime OrderDate { get; set; }

    /// <summary>Gets or sets the total amount.</summary>
    public decimal Total { get; set; }

    public int UserId { get; set; }
}
