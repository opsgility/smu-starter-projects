using Microsoft.EntityFrameworkCore;
using DataForge.Models;

namespace DataForge.Data;

public class AppDbContext : DbContext
{
    public DbSet<Product> Products => Set<Product>();
    public DbSet<Category> Categories => Set<Category>();
    public DbSet<Supplier> Suppliers => Set<Supplier>();
    public DbSet<Tag> Tags => Set<Tag>();
    public DbSet<ProductDetail> ProductDetails => Set<ProductDetail>();

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        optionsBuilder.UseNpgsql("Host=localhost;Database=dataforge;Username=coder;Password=coder");
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // TODO: Configure relationships here (Exercises 1 & 2)
    }
}
