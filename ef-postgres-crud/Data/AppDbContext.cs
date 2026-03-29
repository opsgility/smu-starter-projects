using Microsoft.EntityFrameworkCore;
using DataForge.Models;

namespace DataForge.Data;

public class AppDbContext : DbContext
{
    public DbSet<Product> Products => Set<Product>();
    public DbSet<Category> Categories => Set<Category>();

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        optionsBuilder.UseNpgsql("Host=localhost;Database=dataforge;Username=coder;Password=coder");
    }
}
