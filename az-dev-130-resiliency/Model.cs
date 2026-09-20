using Microsoft.EntityFrameworkCore;

namespace Anchorline.Resiliency;

public class Ping
{
    public int PingId { get; set; }
    public DateTime SentUtc { get; set; }
    public string Payload { get; set; } = "";
}

public class Counter
{
    public int Id { get; set; }
    public long Value { get; set; }
}

public class ResilContext : DbContext
{
    public ResilContext(DbContextOptions<ResilContext> opts) : base(opts) {}
    public DbSet<Ping> Pings => Set<Ping>();
    public DbSet<Counter> Counters => Set<Counter>();
}
