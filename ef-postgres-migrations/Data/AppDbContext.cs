using Microsoft.EntityFrameworkCore;
using DataForge.Models;

namespace DataForge.Data;

public class AppDbContext : DbContext
{
    public DbSet<Product> Products => Set<Product>();
    public DbSet<Category> Categories => Set<Category>();

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        optionsBuilder.UseNpgsql("Host=localhost;Database=dataforge_migrations;Username=coder;Password=coder");
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // TODO: Add HasData() seed data here (Exercise 2)
    }
}
