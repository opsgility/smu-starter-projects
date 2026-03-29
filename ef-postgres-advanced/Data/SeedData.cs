using DataForge.Models;

namespace DataForge.Data;

public static class SeedData
{
    public static void Initialize(AppDbContext context)
    {
        context.Database.EnsureCreated();

        if (context.Products.Any()) return;

        // Categories
        var categories = new List<Category>
        {
            new() { Name = "Electronics", Description = "Electronic devices and components" },
            new() { Name = "Clothing", Description = "Apparel and accessories" },
            new() { Name = "Books", Description = "Physical and digital books" },
            new() { Name = "Home & Garden", Description = "Home improvement and garden supplies" },
            new() { Name = "Sports", Description = "Sports equipment and gear" }
        };
        context.Categories.AddRange(categories);
        context.SaveChanges();

        // Suppliers
        var suppliers = new List<Supplier>
        {
            new() { CompanyName = "TechSource Inc.", ContactEmail = "orders@techsource.com", Phone = "555-0101" },
            new() { CompanyName = "Global Goods Ltd.", ContactEmail = "sales@globalgoods.com", Phone = "555-0102" },
            new() { CompanyName = "Prime Distributors", ContactEmail = "info@primedist.com", Phone = "555-0103" },
            new() { CompanyName = "ValueChain Supply", ContactEmail = "contact@valuechain.com", Phone = "555-0104" }
        };
        context.Suppliers.AddRange(suppliers);
        context.SaveChanges();

        // Tags
        var tags = new List<Tag>
        {
            new() { Name = "Bestseller" },
            new() { Name = "New Arrival" },
            new() { Name = "Clearance" },
            new() { Name = "Premium" },
            new() { Name = "Eco-Friendly" },
            new() { Name = "Limited Edition" }
        };
        context.Tags.AddRange(tags);
        context.SaveChanges();

        // Products (30+ with some marked IsDeleted)
        var products = new List<Product>
        {
            new() { Name = "Wireless Mouse", SKU = "ELEC-001", Price = 29.99m, StockQuantity = 150, CategoryId = categories[0].Id, SupplierId = suppliers[0].Id, IsDeleted = false },
            new() { Name = "USB-C Hub", SKU = "ELEC-002", Price = 49.99m, StockQuantity = 80, CategoryId = categories[0].Id, SupplierId = suppliers[0].Id, IsDeleted = false },
            new() { Name = "Mechanical Keyboard", SKU = "ELEC-003", Price = 89.99m, StockQuantity = 60, CategoryId = categories[0].Id, SupplierId = suppliers[0].Id, IsDeleted = false },
            new() { Name = "Monitor Stand", SKU = "ELEC-004", Price = 39.99m, StockQuantity = 45, CategoryId = categories[0].Id, SupplierId = suppliers[2].Id, IsDeleted = true },
            new() { Name = "Webcam HD", SKU = "ELEC-005", Price = 59.99m, StockQuantity = 90, CategoryId = categories[0].Id, SupplierId = suppliers[0].Id, IsDeleted = false },
            new() { Name = "Bluetooth Speaker", SKU = "ELEC-006", Price = 34.99m, StockQuantity = 120, CategoryId = categories[0].Id, SupplierId = suppliers[2].Id, IsDeleted = false },
            new() { Name = "Laptop Sleeve", SKU = "ELEC-007", Price = 19.99m, StockQuantity = 200, CategoryId = categories[0].Id, SupplierId = suppliers[1].Id, IsDeleted = true },

            new() { Name = "Cotton T-Shirt", SKU = "CLTH-001", Price = 14.99m, StockQuantity = 300, CategoryId = categories[1].Id, SupplierId = suppliers[1].Id, IsDeleted = false },
            new() { Name = "Denim Jeans", SKU = "CLTH-002", Price = 49.99m, StockQuantity = 100, CategoryId = categories[1].Id, SupplierId = suppliers[1].Id, IsDeleted = false },
            new() { Name = "Running Shoes", SKU = "CLTH-003", Price = 79.99m, StockQuantity = 75, CategoryId = categories[1].Id, SupplierId = suppliers[3].Id, IsDeleted = false },
            new() { Name = "Winter Jacket", SKU = "CLTH-004", Price = 129.99m, StockQuantity = 40, CategoryId = categories[1].Id, SupplierId = suppliers[1].Id, IsDeleted = true },
            new() { Name = "Baseball Cap", SKU = "CLTH-005", Price = 12.99m, StockQuantity = 250, CategoryId = categories[1].Id, SupplierId = suppliers[3].Id, IsDeleted = false },
            new() { Name = "Wool Scarf", SKU = "CLTH-006", Price = 24.99m, StockQuantity = 180, CategoryId = categories[1].Id, SupplierId = suppliers[1].Id, IsDeleted = false },

            new() { Name = "C# in Depth", SKU = "BOOK-001", Price = 44.99m, StockQuantity = 50, CategoryId = categories[2].Id, SupplierId = suppliers[2].Id, IsDeleted = false },
            new() { Name = "Clean Code", SKU = "BOOK-002", Price = 39.99m, StockQuantity = 65, CategoryId = categories[2].Id, SupplierId = suppliers[2].Id, IsDeleted = false },
            new() { Name = "Design Patterns", SKU = "BOOK-003", Price = 54.99m, StockQuantity = 30, CategoryId = categories[2].Id, SupplierId = suppliers[2].Id, IsDeleted = false },
            new() { Name = "EF Core in Action", SKU = "BOOK-004", Price = 49.99m, StockQuantity = 40, CategoryId = categories[2].Id, SupplierId = suppliers[2].Id, IsDeleted = false },
            new() { Name = "Outdated SQL Guide", SKU = "BOOK-005", Price = 29.99m, StockQuantity = 15, CategoryId = categories[2].Id, SupplierId = suppliers[2].Id, IsDeleted = true },
            new() { Name = "ASP.NET Core Handbook", SKU = "BOOK-006", Price = 42.99m, StockQuantity = 55, CategoryId = categories[2].Id, SupplierId = suppliers[2].Id, IsDeleted = false },

            new() { Name = "Garden Hose 50ft", SKU = "HOME-001", Price = 34.99m, StockQuantity = 70, CategoryId = categories[3].Id, SupplierId = suppliers[3].Id, IsDeleted = false },
            new() { Name = "LED Desk Lamp", SKU = "HOME-002", Price = 27.99m, StockQuantity = 110, CategoryId = categories[3].Id, SupplierId = suppliers[0].Id, IsDeleted = false },
            new() { Name = "Tool Set 50pc", SKU = "HOME-003", Price = 64.99m, StockQuantity = 35, CategoryId = categories[3].Id, SupplierId = suppliers[3].Id, IsDeleted = false },
            new() { Name = "Plant Pot Set", SKU = "HOME-004", Price = 22.99m, StockQuantity = 90, CategoryId = categories[3].Id, SupplierId = suppliers[3].Id, IsDeleted = false },
            new() { Name = "Old Paint Roller", SKU = "HOME-005", Price = 8.99m, StockQuantity = 5, CategoryId = categories[3].Id, SupplierId = suppliers[3].Id, IsDeleted = true },
            new() { Name = "Smart Thermostat", SKU = "HOME-006", Price = 149.99m, StockQuantity = 25, CategoryId = categories[3].Id, SupplierId = suppliers[0].Id, IsDeleted = false },

            new() { Name = "Yoga Mat", SKU = "SPRT-001", Price = 24.99m, StockQuantity = 160, CategoryId = categories[4].Id, SupplierId = suppliers[3].Id, IsDeleted = false },
            new() { Name = "Dumbbell Set 20lb", SKU = "SPRT-002", Price = 44.99m, StockQuantity = 50, CategoryId = categories[4].Id, SupplierId = suppliers[3].Id, IsDeleted = false },
            new() { Name = "Jump Rope", SKU = "SPRT-003", Price = 9.99m, StockQuantity = 200, CategoryId = categories[4].Id, SupplierId = suppliers[1].Id, IsDeleted = false },
            new() { Name = "Tennis Racket", SKU = "SPRT-004", Price = 69.99m, StockQuantity = 30, CategoryId = categories[4].Id, SupplierId = suppliers[3].Id, IsDeleted = false },
            new() { Name = "Deflated Basketball", SKU = "SPRT-005", Price = 19.99m, StockQuantity = 0, CategoryId = categories[4].Id, SupplierId = suppliers[1].Id, IsDeleted = true },
            new() { Name = "Resistance Bands", SKU = "SPRT-006", Price = 14.99m, StockQuantity = 175, CategoryId = categories[4].Id, SupplierId = suppliers[3].Id, IsDeleted = false },
            new() { Name = "Water Bottle 32oz", SKU = "SPRT-007", Price = 16.99m, StockQuantity = 300, CategoryId = categories[4].Id, SupplierId = suppliers[1].Id, IsDeleted = false },
        };
        context.Products.AddRange(products);
        context.SaveChanges();

        // Assign tags to some products
        products[0].Tags.AddRange(new[] { tags[0], tags[3] });           // Wireless Mouse: Bestseller, Premium
        products[2].Tags.AddRange(new[] { tags[1], tags[3] });           // Mechanical Keyboard: New Arrival, Premium
        products[5].Tags.AddRange(new[] { tags[0] });                    // Bluetooth Speaker: Bestseller
        products[7].Tags.AddRange(new[] { tags[0], tags[4] });           // Cotton T-Shirt: Bestseller, Eco-Friendly
        products[9].Tags.AddRange(new[] { tags[1] });                    // Running Shoes: New Arrival
        products[13].Tags.AddRange(new[] { tags[0], tags[3] });          // C# in Depth: Bestseller, Premium
        products[15].Tags.AddRange(new[] { tags[3] });                   // Design Patterns: Premium
        products[20].Tags.AddRange(new[] { tags[1], tags[4] });          // LED Desk Lamp: New Arrival, Eco-Friendly
        products[25].Tags.AddRange(new[] { tags[4] });                   // Yoga Mat: Eco-Friendly
        products[27].Tags.AddRange(new[] { tags[2] });                   // Jump Rope: Clearance
        products[30].Tags.AddRange(new[] { tags[0], tags[4] });          // Water Bottle: Bestseller, Eco-Friendly
        products[6].Tags.AddRange(new[] { tags[2] });                    // Laptop Sleeve: Clearance (deleted)
        products[10].Tags.AddRange(new[] { tags[2], tags[5] });          // Winter Jacket: Clearance, Limited Edition (deleted)
        context.SaveChanges();
    }
}
