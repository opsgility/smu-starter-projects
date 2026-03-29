using DataForge.Models;

namespace DataForge.Data;

public static class SeedData
{
    public static void Initialize(AppDbContext context)
    {
        context.Database.EnsureCreated();

        if (context.Products.Any()) return;

        // 5 Categories
        var categories = new List<Category>
        {
            new() { Name = "Electronics", Description = "Electronic devices and components" },
            new() { Name = "Clothing", Description = "Apparel and accessories" },
            new() { Name = "Books", Description = "Physical and digital books" },
            new() { Name = "Home & Garden", Description = "Home improvement and garden supplies" },
            new() { Name = "Sports", Description = "Sports equipment and fitness gear" }
        };
        context.Categories.AddRange(categories);
        context.SaveChanges();

        // 6 Suppliers
        var suppliers = new List<Supplier>
        {
            new() { CompanyName = "TechSource Inc.", ContactEmail = "orders@techsource.com", Phone = "555-0101" },
            new() { CompanyName = "Global Goods Ltd.", ContactEmail = "sales@globalgoods.com", Phone = "555-0102" },
            new() { CompanyName = "Prime Distributors", ContactEmail = "info@primedist.com", Phone = "555-0103" },
            new() { CompanyName = "ValueChain Supply", ContactEmail = "contact@valuechain.com", Phone = "555-0104" },
            new() { CompanyName = "QuickShip Direct", ContactEmail = "orders@quickship.com", Phone = "555-0105" },
            new() { CompanyName = "Mega Wholesale", ContactEmail = "bulk@megawholesale.com", Phone = "555-0106" }
        };
        context.Suppliers.AddRange(suppliers);
        context.SaveChanges();

        // 8 Tags
        var tags = new List<Tag>
        {
            new() { Name = "Bestseller" },
            new() { Name = "New Arrival" },
            new() { Name = "Clearance" },
            new() { Name = "Premium" },
            new() { Name = "Eco-Friendly" },
            new() { Name = "Limited Edition" },
            new() { Name = "Budget" },
            new() { Name = "Featured" }
        };
        context.Tags.AddRange(tags);
        context.SaveChanges();

        // 50+ Products spread across categories
        var random = new Random(42); // Fixed seed for reproducibility
        var products = new List<Product>();
        var productNames = new Dictionary<int, string[]>
        {
            [0] = new[] { "Wireless Mouse", "USB-C Hub", "Mechanical Keyboard", "Webcam HD", "Bluetooth Speaker", "Laptop Stand", "Monitor Arm", "Desk Pad XL", "Charging Station", "Noise-Cancelling Headphones", "Smart Watch", "Portable SSD" },
            [1] = new[] { "Cotton T-Shirt", "Denim Jeans", "Running Shoes", "Baseball Cap", "Wool Scarf", "Rain Jacket", "Cargo Shorts", "Dress Shirt", "Hiking Boots", "Beanie Hat" },
            [2] = new[] { "C# in Depth", "Clean Code", "Design Patterns", "EF Core in Action", "ASP.NET Core Handbook", "Docker Deep Dive", "Azure Architecture", "SQL Performance Tuning", "Kubernetes Up & Running", "The Pragmatic Programmer" },
            [3] = new[] { "Garden Hose 50ft", "LED Desk Lamp", "Tool Set 50pc", "Plant Pot Set", "Smart Thermostat", "Door Mat", "Wall Shelf Unit", "Power Drill", "Ceiling Fan", "Kitchen Scale" },
            [4] = new[] { "Yoga Mat", "Dumbbell Set 20lb", "Jump Rope", "Tennis Racket", "Resistance Bands", "Water Bottle 32oz", "Foam Roller", "Boxing Gloves", "Basketball", "Swim Goggles" }
        };

        int skuCounter = 1;
        foreach (var catIndex in Enumerable.Range(0, 5))
        {
            foreach (var name in productNames[catIndex])
            {
                products.Add(new Product
                {
                    Name = name,
                    SKU = $"SKU-{skuCounter++:D4}",
                    Price = Math.Round((decimal)(random.NextDouble() * 150 + 5), 2),
                    StockQuantity = random.Next(5, 500),
                    CategoryId = categories[catIndex].Id,
                    SupplierId = suppliers[random.Next(suppliers.Count)].Id
                });
            }
        }
        context.Products.AddRange(products);
        context.SaveChanges();

        // Assign tags to products
        foreach (var product in products)
        {
            int tagCount = random.Next(0, 4); // 0-3 tags per product
            var shuffledTags = tags.OrderBy(_ => random.Next()).Take(tagCount).ToList();
            product.Tags.AddRange(shuffledTags);
        }
        context.SaveChanges();

        Console.WriteLine($"Seeded {products.Count} products across {categories.Count} categories");
    }
}
