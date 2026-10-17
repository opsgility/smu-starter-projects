using System.Collections.Concurrent;

namespace Halcyon.Adventure.Api.Products;

public sealed class InMemoryProductRepository : IProductRepository
{
    private readonly ConcurrentDictionary<int, Product> _rows = new();
    private int _nextId;

    public InMemoryProductRepository()
    {
        Add(new Product { Sku = "AW-HLM-001", Name = "Sport-100 Helmet, Red", Price = 34.99m, Cost = 13.08m });
        Add(new Product { Sku = "AW-BTL-003", Name = "Water Bottle - 30 oz.", Price = 4.99m, Cost = 1.87m });
    }

    public IReadOnlyList<Product> GetAll() => _rows.Values.OrderBy(p => p.Id).ToList();

    public Product? Get(int id) => _rows.TryGetValue(id, out var p) ? p : null;

    public Product Add(Product product)
    {
        product.Id = Interlocked.Increment(ref _nextId);
        _rows[product.Id] = product;
        return product;
    }

    public bool Update(int id, Action<Product> mutate)
    {
        if (!_rows.TryGetValue(id, out var existing))
        {
            return false;
        }

        mutate(existing);
        return true;
    }

    public bool Delete(int id) => _rows.TryRemove(id, out _);

    public void Clear()
    {
        _rows.Clear();
        _nextId = 0;
    }
}
