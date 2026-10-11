namespace Halcyon.Adventure.Api.Data;

/// <summary>
/// EF Core entity mapped to <c>AdventureWorks.Production.Product</c>.
/// Only the columns the Products API consumes are projected here.
/// </summary>
public class Product
{
    public int ProductID { get; set; }

    public string Name { get; set; } = string.Empty;

    public string ProductNumber { get; set; } = string.Empty;

    public string? Color { get; set; }

    public decimal StandardCost { get; set; }

    public decimal ListPrice { get; set; }

    public string? Size { get; set; }

    public bool MakeFlag { get; set; }

    public bool FinishedGoodsFlag { get; set; }

    public int SafetyStockLevel { get; set; }

    public int ReorderPoint { get; set; }

    public DateTime SellStartDate { get; set; }

    public DateTime? SellEndDate { get; set; }

    public DateTime? DiscontinuedDate { get; set; }

    public DateTime ModifiedDate { get; set; }

    public Guid rowguid { get; set; }
}
