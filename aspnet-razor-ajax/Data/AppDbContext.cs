using Microsoft.EntityFrameworkCore;
using BrightShelf.Models;

namespace BrightShelf.Data;

public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
    {
    }

    public DbSet<Product> Products => Set<Product>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        modelBuilder.Entity<Product>().HasData(
            new Product { Id = 1, Name = "Desk Lamp", Description = "LED desk lamp with adjustable brightness", Price = 29.99m, StockQuantity = 50, Category = "Lighting" },
            new Product { Id = 2, Name = "Wireless Mouse", Description = "Ergonomic wireless mouse", Price = 19.99m, StockQuantity = 120, Category = "Electronics" },
            new Product { Id = 3, Name = "Notebook", Description = "Hardcover lined notebook, 200 pages", Price = 12.50m, StockQuantity = 300, Category = "Stationery" },
            new Product { Id = 4, Name = "USB-C Hub", Description = "7-port USB-C hub with HDMI", Price = 45.00m, StockQuantity = 80, Category = "Electronics" },
            new Product { Id = 5, Name = "Standing Desk Mat", Description = "Anti-fatigue standing desk mat", Price = 39.99m, StockQuantity = 60, Category = "Furniture" }
        );
    }
}
