using BrightShelf.Models;

namespace BrightShelf;

public static class ProductStore
{
    private static readonly List<Product> _products = new()
    {
        new Product { Id = 1, Name = "Wireless Mouse", Price = 29.99m, Description = "Ergonomic wireless mouse with USB receiver." },
        new Product { Id = 2, Name = "Mechanical Keyboard", Price = 79.99m, Description = "RGB mechanical keyboard with Cherry MX switches." },
        new Product { Id = 3, Name = "USB-C Hub", Price = 49.99m, Description = "7-in-1 USB-C hub with HDMI and ethernet." }
    };

    private static int _nextId = 4;

    public static List<Product> GetAll() => _products.ToList();

    public static Product? GetById(int id) => _products.FirstOrDefault(p => p.Id == id);

    public static void Add(Product product)
    {
        product.Id = _nextId++;
        _products.Add(product);
    }

    public static void Update(Product product)
    {
        var existing = _products.FirstOrDefault(p => p.Id == product.Id);
        if (existing != null)
        {
            existing.Name = product.Name;
            existing.Price = product.Price;
            existing.Description = product.Description;
        }
    }

    public static void Delete(int id)
    {
        var product = _products.FirstOrDefault(p => p.Id == id);
        if (product != null)
        {
            _products.Remove(product);
        }
    }
}
