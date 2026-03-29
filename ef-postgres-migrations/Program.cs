using DataForge.Data;

Console.WriteLine("=== DataForge Product Catalog - Migrations ===\n");

// NOTE: Do NOT call EnsureCreated() — we'll use migrations instead!
// Follow the exercise instructions to create and apply migrations.

using var db = new AppDbContext();
Console.WriteLine("DbContext ready. Use 'dotnet ef migrations add' to create your first migration.");
