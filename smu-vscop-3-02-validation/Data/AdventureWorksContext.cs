using Microsoft.EntityFrameworkCore;

namespace Halcyon.Adventure.Api.Data;

/// <summary>
/// Narrow DbContext projecting only the Production schema the Products API uses.
/// The full AdventureWorks schema is reverse-engineered in Course 4; this starter
/// stays small on purpose.
/// </summary>
public class AdventureWorksContext : DbContext
{
    public AdventureWorksContext(DbContextOptions<AdventureWorksContext> options)
        : base(options)
    {
    }

    public DbSet<Product> Products => Set<Product>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Product>(entity =>
        {
            entity.ToTable("Product", schema: "Production");
            entity.HasKey(p => p.ProductID);
            entity.Property(p => p.Name).HasMaxLength(50).IsRequired();
            entity.Property(p => p.ProductNumber).HasMaxLength(25).IsRequired();
            entity.Property(p => p.Color).HasMaxLength(15);
            entity.Property(p => p.Size).HasMaxLength(5);
            entity.Property(p => p.StandardCost).HasColumnType("money");
            entity.Property(p => p.ListPrice).HasColumnType("money");
        });
    }
}
