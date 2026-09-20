using DataForge.Data;
using DataForge.Models;
using Microsoft.EntityFrameworkCore;

Console.WriteLine("=== DataForge Advanced Queries ===\n");

using var context = new AppDbContext();
SeedData.Initialize(context);

// ==============================================
// EXERCISE 1: Global Query Filters
// ==============================================
// Notice that deleted products appear in results below.
// Go to AppDbContext.cs and add a global query filter:
//   modelBuilder.Entity<Product>().HasQueryFilter(p => !p.IsDeleted);
// Then re-run to see the difference.

Console.WriteLine("--- All Products (before filter) ---");
var allProducts = context.Products.Include(p => p.Category).ToList();
Console.WriteLine($"Total products: {allProducts.Count}");
foreach (var p in allProducts.Take(10))
{
    Console.WriteLine($"  {p.Name} | Category: {p.Category.Name} | Deleted: {p.IsDeleted}");
}
Console.WriteLine();

// ==============================================
// EXERCISE 2: IgnoreQueryFilters
// ==============================================
// After adding the global query filter above, use IgnoreQueryFilters()
// to retrieve ALL products including soft-deleted ones.

// TODO: Write a query using .IgnoreQueryFilters() to get all products
// Console.WriteLine("--- All Products (ignoring filter) ---");

Console.WriteLine();

// ==============================================
// EXERCISE 3: Complex Where Clauses
// ==============================================
// Find products that are:
//   - In the "Electronics" category AND priced over $40
//   - OR in the "Sports" category AND have stock > 100

// TODO: Write the query
// Console.WriteLine("--- Complex Where Results ---");

Console.WriteLine();

// ==============================================
// EXERCISE 4: Ordering and Paging
// ==============================================
// Get the 2nd page of products (page size = 5), ordered by Price descending

// TODO: Write the query using .OrderByDescending(), .Skip(), .Take()
// Console.WriteLine("--- Page 2 (5 per page, by price desc) ---");

Console.WriteLine();

// ==============================================
// EXERCISE 5: Projections with Select
// ==============================================
// Project products into an anonymous type with:
//   ProductName, CategoryName, SupplierName, TagCount

// TODO: Write the query using .Select()
// Console.WriteLine("--- Product Projections ---");

Console.WriteLine();

// ==============================================
// EXERCISE 6: Grouping
// ==============================================
// Group products by Category and show:
//   CategoryName, ProductCount, AveragePrice, TotalStock

// TODO: Write the query using .GroupBy()
// Console.WriteLine("--- Products Grouped by Category ---");

Console.WriteLine();

// ==============================================
// EXERCISE 7: Any, All, Contains
// ==============================================
// a) Check if ANY product costs more than $100
// b) Check if ALL electronics are priced above $10
// c) Find products whose names contain "Set"

// TODO: Write the queries
// Console.WriteLine("--- Any / All / Contains ---");

Console.WriteLine();

// ==============================================
// EXERCISE 8: Raw SQL with FromSqlRaw
// ==============================================
// Use FromSqlRaw to find products with price > 50
// Remember to use parameterized queries for safety!

// TODO: Write the query using .FromSqlRaw() or .FromSqlInterpolated()
// Console.WriteLine("--- Raw SQL Results ---");

Console.WriteLine();

// ==============================================
// EXERCISE 9: Many-to-Many Queries
// ==============================================
// a) Find all products tagged as "Bestseller"
// b) Find products that have BOTH "Bestseller" AND "Premium" tags
// c) List all tags with their product counts

// TODO: Write the queries
// Console.WriteLine("--- Many-to-Many Queries ---");

Console.WriteLine();

Console.WriteLine("=== Advanced Queries Complete ===");
