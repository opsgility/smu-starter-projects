using DataForge.Models;

namespace DataForge.Data;

public static class SeedData
{
    public static void Initialize(AppDbContext context)
    {
        context.Database.EnsureCreated();

        if (context.Products.Any()) return;

        var categories = new List<Category>
        {
            new() { Name = "Electronics", Description = "Electronic devices and accessories" },
            new() { Name = "Clothing", Description = "Apparel and fashion items" },
            new() { Name = "Books", Description = "Physical and digital books" }
        };
        context.Categories.AddRange(categories);
        context.SaveChanges();

        var products = new List<Product>
        {
            new() { Name = "Wireless Mouse", Price = 29.99m, Description = "Ergonomic wireless mouse with USB receiver", StockQuantity = 150, CategoryId = categories[0].Id },
            new() { Name = "USB-C Hub", Price = 49.99m, Description = "7-port USB-C hub with HDMI output", StockQuantity = 80, CategoryId = categories[0].Id },
            new() { Name = "Mechanical Keyboard", Price = 89.99m, Description = "Cherry MX Blue switches, RGB backlit", StockQuantity = 60, CategoryId = categories[0].Id },
            new() { Name = "Cotton T-Shirt", Price = 14.99m, Description = "100% organic cotton, available in multiple colors", StockQuantity = 300, CategoryId = categories[1].Id },
            new() { Name = "Denim Jeans", Price = 49.99m, Description = "Classic fit denim jeans", StockQuantity = 100, CategoryId = categories[1].Id },
            new() { Name = "C# in Depth", Price = 44.99m, Description = "Comprehensive guide to C# by Jon Skeet", StockQuantity = 50, CategoryId = categories[2].Id },
            new() { Name = "Clean Code", Price = 39.99m, Description = "A handbook of agile software craftsmanship", StockQuantity = 65, CategoryId = categories[2].Id },
        };
        context.Products.AddRange(products);
        context.SaveChanges();
    }
}
