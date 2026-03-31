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
    public DbSet<Category> Categories => Set<Category>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        modelBuilder.Entity<Category>().HasData(
            new Category { Id = 1, Name = "Electronics", Description = "Electronic devices and accessories" },
            new Category { Id = 2, Name = "Furniture", Description = "Office and home furniture" },
            new Category { Id = 3, Name = "Stationery", Description = "Office supplies and stationery" },
            new Category { Id = 4, Name = "Lighting", Description = "Lamps and lighting solutions" },
            new Category { Id = 5, Name = "Accessories", Description = "Misc accessories" }
        );

        modelBuilder.Entity<Product>().HasData(
            new Product { Id = 1, Name = "Desk Lamp", Description = "LED desk lamp with adjustable brightness", Price = 29.99m, StockQuantity = 50, CategoryId = 4 },
            new Product { Id = 2, Name = "Wireless Mouse", Description = "Ergonomic wireless mouse", Price = 19.99m, StockQuantity = 120, CategoryId = 1 },
            new Product { Id = 3, Name = "Notebook", Description = "Hardcover lined notebook, 200 pages", Price = 12.50m, StockQuantity = 300, CategoryId = 3 },
            new Product { Id = 4, Name = "USB-C Hub", Description = "7-port USB-C hub with HDMI", Price = 45.00m, StockQuantity = 80, CategoryId = 1 },
            new Product { Id = 5, Name = "Standing Desk Mat", Description = "Anti-fatigue standing desk mat", Price = 39.99m, StockQuantity = 60, CategoryId = 2 }
        );
    }
}
