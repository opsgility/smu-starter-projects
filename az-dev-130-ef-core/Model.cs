using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace Anchorline.Orders;

public class Customer
{
    public int CustomerId { get; set; }
    [MaxLength(80)] public string Name { get; set; } = "";
    [MaxLength(200)] public string Email { get; set; } = "";
    public List<Order> Orders { get; set; } = new();
}

public class Product
{
    public int ProductId { get; set; }
    [MaxLength(120)] public string Name { get; set; } = "";
    [MaxLength(40)] public string Sku { get; set; } = "";
    [Column(TypeName = "decimal(10,2)")]
    public decimal Price { get; set; }
}

public class Order
{
    public int OrderId { get; set; }
    public int CustomerId { get; set; }
    public Customer Customer { get; set; } = null!;
    public DateTime PlacedUtc { get; set; }
    [MaxLength(30)] public string Status { get; set; } = "New";
    public List<OrderLine> OrderLines { get; set; } = new();
}

public class OrderLine
{
    public int OrderLineId { get; set; }
    public int OrderId { get; set; }
    public Order Order { get; set; } = null!;
    public int ProductId { get; set; }
    public Product Product { get; set; } = null!;
    public int Quantity { get; set; }
    [Column(TypeName = "decimal(10,2)")]
    public decimal UnitPrice { get; set; }
}
