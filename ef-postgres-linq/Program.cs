using DataForge.Data;
using DataForge.Models;
using Microsoft.EntityFrameworkCore;

Console.WriteLine("=== DataForge Analytics Dashboard - LINQ Queries ===\n");

using var db = new AppDbContext();
db.Database.EnsureCreated();
SeedData.Initialize(db);

Console.WriteLine("Data loaded. Follow the exercise instructions to write LINQ queries.\n");

// --- Exercise 1: Filtering, Sorting, and Paging ---
// Write your queries below:


// --- Exercise 2: Projections, Grouping, and Aggregation ---
// Write your queries below:
