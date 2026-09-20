using DataForge.Models;

namespace DataForge.Data;

public static class SeedData
{
    public static void Initialize(AppDbContext db)
    {
        if (db.Products.Any()) return;

        var categories = new[]
        {
            new Category { Name = "Electronics", Description = "Electronic devices" },
            new Category { Name = "Books", Description = "Physical and digital books" },
            new Category { Name = "Clothing", Description = "Apparel and accessories" },
            new Category { Name = "Home & Garden", Description = "Home improvement" },
            new Category { Name = "Sports", Description = "Sports equipment" }
        };
        db.Categories.AddRange(categories);
        db.SaveChanges();

        var suppliers = new[]
        {
            new Supplier { CompanyName = "TechHub Inc", ContactEmail = "sales@techhub.com", Phone = "555-0101" },
            new Supplier { CompanyName = "BookWorld Ltd", ContactEmail = "orders@bookworld.com", Phone = "555-0102" },
            new Supplier { CompanyName = "StyleCraft Co", ContactEmail = "info@stylecraft.com", Phone = "555-0103" }
        };
        db.Suppliers.AddRange(suppliers);
        db.SaveChanges();

        var tags = new[]
        {
            new Tag { Name = "Sale" }, new Tag { Name = "New Arrival" },
            new Tag { Name = "Best Seller" }, new Tag { Name = "Clearance" },
            new Tag { Name = "Premium" }, new Tag { Name = "Eco-Friendly" }
        };
        db.Tags.AddRange(tags);
        db.SaveChanges();

        var products = new List<Product>
        {
            new() { Name = "Wireless Mouse", Price = 29.99m, StockQuantity = 150, CategoryId = categories[0].Id, SupplierId = suppliers[0].Id },
            new() { Name = "Mechanical Keyboard", Price = 89.99m, StockQuantity = 75, CategoryId = categories[0].Id, SupplierId = suppliers[0].Id },
            new() { Name = "USB-C Hub", Price = 45.00m, StockQuantity = 200, CategoryId = categories[0].Id, SupplierId = suppliers[0].Id },
            new() { Name = "Monitor Stand", Price = 35.00m, StockQuantity = 50, CategoryId = categories[0].Id, SupplierId = suppliers[0].Id },
            new() { Name = "Webcam HD", Price = 65.00m, StockQuantity = 30, CategoryId = categories[0].Id, SupplierId = suppliers[0].Id },
            new() { Name = "C# in Depth", Price = 49.99m, StockQuantity = 100, CategoryId = categories[1].Id, SupplierId = suppliers[1].Id },
            new() { Name = "Clean Code", Price = 39.99m, StockQuantity = 120, CategoryId = categories[1].Id, SupplierId = suppliers[1].Id },
            new() { Name = "Design Patterns", Price = 54.99m, StockQuantity = 80, CategoryId = categories[1].Id, SupplierId = suppliers[1].Id },
            new() { Name = "The Pragmatic Programmer", Price = 44.99m, StockQuantity = 90, CategoryId = categories[1].Id, SupplierId = suppliers[1].Id },
            new() { Name = "Developer T-Shirt", Price = 24.99m, StockQuantity = 300, CategoryId = categories[2].Id, SupplierId = suppliers[2].Id },
            new() { Name = "Hoodie", Price = 59.99m, StockQuantity = 150, CategoryId = categories[2].Id, SupplierId = suppliers[2].Id },
            new() { Name = "Laptop Backpack", Price = 79.99m, StockQuantity = 60, CategoryId = categories[2].Id, SupplierId = suppliers[2].Id },
            new() { Name = "Desk Lamp", Price = 32.00m, StockQuantity = 45, CategoryId = categories[3].Id, SupplierId = suppliers[0].Id },
            new() { Name = "Ergonomic Chair Mat", Price = 28.00m, StockQuantity = 70, CategoryId = categories[3].Id, SupplierId = suppliers[0].Id },
            new() { Name = "Cable Organizer", Price = 12.99m, StockQuantity = 500, CategoryId = categories[3].Id, SupplierId = suppliers[0].Id },
            new() { Name = "Standing Desk Converter", Price = 199.99m, StockQuantity = 20, CategoryId = categories[3].Id, SupplierId = suppliers[0].Id },
            new() { Name = "Yoga Mat", Price = 25.00m, StockQuantity = 200, CategoryId = categories[4].Id, SupplierId = suppliers[2].Id },
            new() { Name = "Resistance Bands", Price = 15.99m, StockQuantity = 350, CategoryId = categories[4].Id, SupplierId = suppliers[2].Id },
            new() { Name = "Water Bottle", Price = 18.99m, StockQuantity = 400, CategoryId = categories[4].Id, SupplierId = suppliers[2].Id },
            new() { Name = "Fitness Tracker", Price = 129.99m, StockQuantity = 85, CategoryId = categories[4].Id, SupplierId = suppliers[0].Id },
            new() { Name = "Jump Rope", Price = 9.99m, StockQuantity = 250, CategoryId = categories[4].Id, SupplierId = suppliers[2].Id },
            new() { Name = "Noise Cancelling Headphones", Price = 249.99m, StockQuantity = 40, CategoryId = categories[0].Id, SupplierId = suppliers[0].Id, IsActive = false },
            new() { Name = "Old Edition Textbook", Price = 19.99m, StockQuantity = 5, CategoryId = categories[1].Id, SupplierId = suppliers[1].Id, IsActive = false }
        };
        db.Products.AddRange(products);
        db.SaveChanges();

        // Add tags to some products
        products[0].Tags.Add(tags[1]); // Wireless Mouse - New Arrival
        products[0].Tags.Add(tags[2]); // Wireless Mouse - Best Seller
        products[1].Tags.Add(tags[4]); // Keyboard - Premium
        products[5].Tags.Add(tags[2]); // C# in Depth - Best Seller
        products[6].Tags.Add(tags[2]); // Clean Code - Best Seller
        products[9].Tags.Add(tags[0]); // T-Shirt - Sale
        products[10].Tags.Add(tags[1]); // Hoodie - New Arrival
        products[15].Tags.Add(tags[4]); // Standing Desk - Premium
        products[15].Tags.Add(tags[5]); // Standing Desk - Eco-Friendly
        products[21].Tags.Add(tags[3]); // Headphones - Clearance
        db.SaveChanges();

        Console.WriteLine($"Seed data loaded: {categories.Length} categories, {suppliers.Length} suppliers, {products.Count} products, {tags.Length} tags");
    }
}
