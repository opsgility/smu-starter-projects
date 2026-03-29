using DataForge.Data;
using DataForge.Models;
using Microsoft.EntityFrameworkCore;

Console.WriteLine("=== DataForge Product Catalog - CRUD Operations ===\n");

using var db = new AppDbContext();
db.Database.EnsureCreated();
SeedData.Initialize(db);

// Display current data
var products = db.Products.Include(p => p.Category).ToList();
Console.WriteLine($"Products in catalog: {products.Count}\n");

foreach (var p in products)
{
    Console.WriteLine($"  [{p.Id}] {p.Name} - ${p.Price:F2} ({p.Category?.Name ?? "No Category"})");
}

Console.WriteLine("\n--- Follow the exercise instructions to practice CRUD operations ---");
