using Microsoft.EntityFrameworkCore;
using DataForge.Models;

namespace DataForge.Data;

public class AppDbContext : DbContext
{
    // TODO: Add DbSet properties for your entities here
    // Example: public DbSet<Product> Products => Set<Product>();

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        optionsBuilder.UseNpgsql("Host=localhost;Database=dataforge;Username=coder;Password=coder");
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // TODO: Add Fluent API configuration here (Exercise 2)
    }
}
