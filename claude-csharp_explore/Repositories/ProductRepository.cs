using ECommerceApi.Models;

namespace ECommerceApi.Repositories;

public class ProductRepository : IProductRepository
{
    private static readonly List<Product> _products = new()
    {
        new Product { Id = 1, Name = "Laptop", Price = 999.99m, Category = "Electronics", StockQuantity = 50 },
        new Product { Id = 2, Name = "Mouse", Price = 29.99m, Category = "Accessories", StockQuantity = 200 },
        new Product { Id = 3, Name = "Keyboard", Price = 79.99m, Category = "Accessories", StockQuantity = 150 },
        new Product { Id = 4, Name = "Monitor", Price = 449.99m, Category = "Electronics", StockQuantity = 30 },
        new Product { Id = 5, Name = "Headphones", Price = 149.99m, Category = "Accessories", StockQuantity = 100 }
    };

    private static int _nextId = 6;

    public IEnumerable<Product> GetAll() => _products.ToList();

    public Product? GetById(int id) => _products.FirstOrDefault(p => p.Id == id);

    public Product Create(Product product)
    {
        product.Id = _nextId++;
        _products.Add(product);
        return product;
    }

    public Product? Update(Product product)
    {
        var existing = _products.FirstOrDefault(p => p.Id == product.Id);
        if (existing == null) return null;

        existing.Name = product.Name;
        existing.Price = product.Price;
        existing.Category = product.Category;
        existing.StockQuantity = product.StockQuantity;
        return existing;
    }

    public bool Delete(int id)
    {
        var product = _products.FirstOrDefault(p => p.Id == id);
        if (product == null) return false;
        _products.Remove(product);
        return true;
    }
}
