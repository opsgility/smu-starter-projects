using DataForge.Data;
using Microsoft.EntityFrameworkCore;

Console.WriteLine("=== DataForge Product Catalog - Model Design ===\n");

using var db = new AppDbContext();
db.Database.EnsureCreated();

Console.WriteLine("Database created successfully!");
Console.WriteLine("Follow the exercise instructions to design your entity models.");
