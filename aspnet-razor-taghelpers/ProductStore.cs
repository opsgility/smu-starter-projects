using BrightShelf.Models;

namespace BrightShelf;

public static class ProductStore
{
    private static readonly List<Category> _categories = new()
    {
        new Category { Id = 1, Name = "Electronics" },
        new Category { Id = 2, Name = "Accessories" },
        new Category { Id = 3, Name = "Peripherals" }
    };

    private static readonly List<Product> _products = new()
    {
        new Product { Id = 1, Name = "Wireless Mouse", Price = 29.99m, Description = "Ergonomic wireless mouse with USB receiver.", CategoryId = 3 },
        new Product { Id = 2, Name = "Mechanical Keyboard", Price = 79.99m, Description = "RGB mechanical keyboard with Cherry MX switches.", CategoryId = 3 },
        new Product { Id = 3, Name = "USB-C Hub", Price = 49.99m, Description = "7-in-1 USB-C hub with HDMI and ethernet.", CategoryId = 2 },
        new Product { Id = 4, Name = "Monitor Stand", Price = 39.99m, Description = "Adjustable monitor stand with cable management.", CategoryId = 2 }
    };

    private static int _nextId = 5;

    public static List<Product> GetAll() => _products.ToList();
    public static Product? GetById(int id) => _products.FirstOrDefault(p => p.Id == id);
    public static List<Category> GetCategories() => _categories.ToList();
    public static Category? GetCategoryById(int id) => _categories.FirstOrDefault(c => c.Id == id);

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
            existing.CategoryId = product.CategoryId;
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
