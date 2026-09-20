using DataForge.Models;

namespace DataForge.Data;

public static class SeedData
{
    public static void Initialize(AppDbContext db)
    {
        if (db.Products.Any()) return;

        var electronics = new Category { Name = "Electronics", Description = "Electronic devices and gadgets" };
        var books = new Category { Name = "Books", Description = "Physical and digital books" };
        var clothing = new Category { Name = "Clothing", Description = "Apparel and accessories" };

        db.Categories.AddRange(electronics, books, clothing);
        db.SaveChanges();

        db.Products.AddRange(
            new Product { Name = "Wireless Mouse", Price = 29.99m, Description = "Ergonomic wireless mouse", CategoryId = electronics.Id },
            new Product { Name = "Mechanical Keyboard", Price = 89.99m, Description = "RGB mechanical keyboard", CategoryId = electronics.Id },
            new Product { Name = "USB-C Hub", Price = 45.00m, Description = "7-in-1 USB-C hub", CategoryId = electronics.Id },
            new Product { Name = "Monitor Stand", Price = 35.00m, Description = "Adjustable monitor stand", CategoryId = electronics.Id },
            new Product { Name = "C# in Depth", Price = 49.99m, Description = "Advanced C# programming", CategoryId = books.Id },
            new Product { Name = "Clean Code", Price = 39.99m, Description = "Software craftsmanship guide", CategoryId = books.Id },
            new Product { Name = "Design Patterns", Price = 54.99m, Description = "Gang of Four patterns", CategoryId = books.Id },
            new Product { Name = "Developer T-Shirt", Price = 24.99m, Description = "Cotton developer tee", CategoryId = clothing.Id },
            new Product { Name = "Hoodie", Price = 59.99m, Description = "Warm zip-up hoodie", CategoryId = clothing.Id },
            new Product { Name = "Laptop Backpack", Price = 79.99m, Description = "Waterproof laptop backpack", CategoryId = clothing.Id }
        );
        db.SaveChanges();

        Console.WriteLine("Seed data loaded: 3 categories, 10 products");
    }
}
