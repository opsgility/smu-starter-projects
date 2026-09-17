using Microsoft.EntityFrameworkCore;

namespace Anchorline.Orders;

public class OrderContext : DbContext
{
    public OrderContext(DbContextOptions<OrderContext> options) : base(options) { }

    public DbSet<Customer> Customers => Set<Customer>();
    public DbSet<Product>  Products  => Set<Product>();
    public DbSet<Order>    Orders    => Set<Order>();
    public DbSet<OrderLine> OrderLines => Set<OrderLine>();

    protected override void OnModelCreating(ModelBuilder mb)
    {
        mb.Entity<Customer>().HasIndex(c => c.Email).IsUnique();
        mb.Entity<Product>().HasIndex(p => p.Sku).IsUnique();
        mb.Entity<Order>().HasIndex(o => o.PlacedUtc);
    }
}
