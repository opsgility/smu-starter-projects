using Microsoft.EntityFrameworkCore;
using DataForge.Models;

namespace DataForge.Data;

public class AppDbContext : DbContext
{
    public DbSet<Product> Products => Set<Product>();
    public DbSet<Category> Categories => Set<Category>();

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        optionsBuilder.UseNpgsql("Host=localhost;Database=dataforge_validation;Username=postgres;Password=postgres");
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // Category configuration
        modelBuilder.Entity<Category>(entity =>
        {
            entity.HasKey(c => c.Id);
            entity.Property(c => c.Name).IsRequired().HasMaxLength(100);
            entity.Property(c => c.Description).HasMaxLength(500);
        });

        // Product configuration
        modelBuilder.Entity<Product>(entity =>
        {
            entity.HasKey(p => p.Id);
            entity.Property(p => p.Name).HasMaxLength(200);
            entity.Property(p => p.Price).HasColumnType("decimal(18,2)");
            entity.Property(p => p.Description).HasMaxLength(1000);

            // PostgreSQL concurrency using xmin system column
            entity.UseXminAsConcurrencyToken();

            // Ignore RowVersion for PostgreSQL — xmin is used instead
            entity.Ignore(p => p.RowVersion);

            entity.HasOne(p => p.Category)
                  .WithMany(c => c.Products)
                  .HasForeignKey(p => p.CategoryId)
                  .OnDelete(DeleteBehavior.Restrict);
        });
    }
}
