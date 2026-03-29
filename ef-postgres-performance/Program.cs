using DataForge.Data;
using DataForge.Models;
using Microsoft.EntityFrameworkCore;
using System.Diagnostics;

Console.WriteLine("=== DataForge Performance Lab ===");
Console.WriteLine("Watch the SQL output below — find and fix the performance problems!\n");

using var context = new AppDbContext();
SeedData.Initialize(context);

// ==============================================
// PROBLEM 1: N+1 Query Problem
// ==============================================
// This code loads all categories, then accesses .Products for each one.
// Without .Include(), EF Core issues a SEPARATE SQL query for each category!
// Watch the console output — you'll see multiple SELECT statements.
//
// FIX: Add .Include(c => c.Products) to the initial query.

Console.WriteLine("--- Problem 1: N+1 Query (Categories -> Products) ---");
var sw = Stopwatch.StartNew();

var categories = context.Categories.ToList(); // No Include!

foreach (var category in categories)
{
    // This triggers a LAZY LOAD or returns empty (depending on config)
    // Each access generates a separate SQL query!
    var productCount = context.Products.Where(p => p.CategoryId == category.Id).Count();
    var totalValue = context.Products
        .Where(p => p.CategoryId == category.Id)
        .Sum(p => p.Price * p.StockQuantity);

    Console.WriteLine($"  {category.Name}: {productCount} products, Total inventory value: {totalValue:C}");
}

sw.Stop();
Console.WriteLine($"  Time: {sw.ElapsedMilliseconds}ms");
Console.WriteLine();

// ==============================================
// PROBLEM 2: Loading Too Much Data
// ==============================================
// This loads ENTIRE product entities when we only need names and prices.
// It also loads ALL products when we only display the top 10.
//
// FIX: Use .Select() projection and .Take(10)

Console.WriteLine("--- Problem 2: Over-fetching Data ---");
sw.Restart();

var allProducts = context.Products
    .Include(p => p.Category)
    .Include(p => p.Supplier)
    .Include(p => p.Tags)
    .ToList(); // Loads EVERYTHING into memory!

// But we only need the top 10 most expensive with name and price...
var topProducts = allProducts
    .OrderByDescending(p => p.Price)
    .Take(10);

foreach (var p in topProducts)
{
    Console.WriteLine($"  {p.Name} - {p.Price:C}");
}

sw.Stop();
Console.WriteLine($"  Time: {sw.ElapsedMilliseconds}ms");
Console.WriteLine();

// ==============================================
// PROBLEM 3: Repeated Queries in a Loop
// ==============================================
// This code queries the database inside a loop for each supplier.
// Each iteration hits the database separately.
//
// FIX: Load all data in ONE query, then process in memory.

Console.WriteLine("--- Problem 3: Queries Inside a Loop ---");
sw.Restart();

var supplierIds = context.Suppliers.Select(s => s.Id).ToList();

foreach (var supplierId in supplierIds)
{
    // Each of these is a separate database round-trip!
    var supplier = context.Suppliers.Find(supplierId)!;
    var products = context.Products.Where(p => p.SupplierId == supplierId).ToList();
    var avgPrice = products.Any() ? products.Average(p => p.Price) : 0;

    Console.WriteLine($"  {supplier.CompanyName}: {products.Count} products, Avg price: {avgPrice:C}");
}

sw.Stop();
Console.WriteLine($"  Time: {sw.ElapsedMilliseconds}ms");
Console.WriteLine();

// ==============================================
// PROBLEM 4: Tracking Overhead on Read-Only Queries
// ==============================================
// This loads products with change tracking enabled,
// but we never modify them — just read and display.
//
// FIX: Add .AsNoTracking() for read-only queries.

Console.WriteLine("--- Problem 4: Unnecessary Change Tracking ---");
sw.Restart();

var readOnlyProducts = context.Products
    .Include(p => p.Category)
    .OrderBy(p => p.Name)
    .ToList(); // Tracked by default — unnecessary overhead!

Console.WriteLine($"  Loaded {readOnlyProducts.Count} products (read-only display)");
foreach (var p in readOnlyProducts.Take(5))
{
    Console.WriteLine($"  {p.Name} | {p.Category.Name} | {p.Price:C}");
}

sw.Stop();
Console.WriteLine($"  Time: {sw.ElapsedMilliseconds}ms");
Console.WriteLine();

// ==============================================
// PROBLEM 5: No Projection for Aggregates
// ==============================================
// This loads full entities just to compute aggregates.
//
// FIX: Use GroupBy + Select with aggregates directly in the query.

Console.WriteLine("--- Problem 5: Aggregates Without Projection ---");
sw.Restart();

var allProductsAgain = context.Products.Include(p => p.Category).ToList();

var report = allProductsAgain
    .GroupBy(p => p.Category.Name)
    .Select(g => new
    {
        Category = g.Key,
        Count = g.Count(),
        AvgPrice = g.Average(p => p.Price),
        MaxPrice = g.Max(p => p.Price),
        TotalStock = g.Sum(p => p.StockQuantity)
    })
    .OrderByDescending(r => r.TotalStock);

foreach (var r in report)
{
    Console.WriteLine($"  {r.Category}: {r.Count} items, Avg: {r.AvgPrice:C}, Max: {r.MaxPrice:C}, Stock: {r.TotalStock}");
}

sw.Stop();
Console.WriteLine($"  Time: {sw.ElapsedMilliseconds}ms");
Console.WriteLine();

Console.WriteLine("=== Review the SQL output above and optimize each problem! ===");
