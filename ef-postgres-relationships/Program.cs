using DataForge.Data;
using Microsoft.EntityFrameworkCore;

Console.WriteLine("=== DataForge Product Catalog - Entity Relationships ===\n");

using var db = new AppDbContext();
db.Database.EnsureCreated();

Console.WriteLine("Database created. Follow the exercise instructions to configure relationships.");
