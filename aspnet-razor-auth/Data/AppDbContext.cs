using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;
using BrightShelf.Models;

namespace BrightShelf.Data;

public class AppDbContext : IdentityDbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
    {
    }

    public DbSet<Product> Products => Set<Product>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        modelBuilder.Entity<Product>().HasData(
            new Product { Id = 1, Name = "Desk Lamp", Description = "LED desk lamp with adjustable brightness", Price = 29.99m, StockQuantity = 50 },
            new Product { Id = 2, Name = "Wireless Mouse", Description = "Ergonomic wireless mouse", Price = 19.99m, StockQuantity = 120 },
            new Product { Id = 3, Name = "Notebook", Description = "Hardcover lined notebook, 200 pages", Price = 12.50m, StockQuantity = 300 }
        );
    }
}
