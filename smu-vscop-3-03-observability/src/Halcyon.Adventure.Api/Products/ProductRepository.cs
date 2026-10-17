using System.Collections.Concurrent;

namespace Halcyon.Adventure.Api.Products;

/// <summary>
/// In-memory product store seeded with four canonical Adventure Works bikes.
/// Course 4 (EF Core) replaces this with a real DbContext.
/// </summary>
public sealed class ProductRepository : IProductRepository
{
    private readonly ConcurrentDictionary<int, Product> _store = new();
    private int _nextId;

    public ProductRepository()
    {
        var today = DateOnly.FromDateTime(DateTime.UtcNow);
        Seed(new Product(1, "Mountain-100 Silver, 38", "BK-M68S-38", 1912.15m, 3399.99m, today, null, DateTime.UtcNow));
        Seed(new Product(2, "Mountain-100 Silver, 42", "BK-M68S-42", 1912.15m, 3399.99m, today, null, DateTime.UtcNow));
        Seed(new Product(3, "Mountain-100 Black, 38", "BK-M68B-38", 1898.09m, 3374.99m, today, null, DateTime.UtcNow));
        Seed(new Product(4, "Road-150 Red, 62", "BK-R93R-62", 2171.29m, 3578.27m, today, null, DateTime.UtcNow));
        _nextId = 5;
    }

    private void Seed(Product product) => _store[product.ProductId] = product;

    public IReadOnlyCollection<Product> GetAll() => _store.Values.ToArray();

    public bool TryGet(int id, out Product? product)
    {
        var found = _store.TryGetValue(id, out var value);
        product = value;
        return found;
    }

    public Product Create(CreateProductRequest request)
    {
        var id = Interlocked.Increment(ref _nextId);
        var product = new Product(
            id,
            request.Name,
            request.ProductNumber,
            request.StandardCost,
            request.ListPrice,
            request.SellStartDate,
            request.SellEndDate,
            DateTime.UtcNow);
        _store[id] = product;
        return product;
    }

    public Product Update(int id, UpdateProductRequest request)
    {
        var existing = _store[id];
        var updated = existing with
        {
            Name = request.Name,
            StandardCost = request.StandardCost,
            ListPrice = request.ListPrice,
            SellStartDate = request.SellStartDate,
            SellEndDate = request.SellEndDate,
            ModifiedDate = DateTime.UtcNow,
        };
        _store[id] = updated;
        return updated;
    }

    public bool Delete(int id) => _store.TryRemove(id, out _);
}
