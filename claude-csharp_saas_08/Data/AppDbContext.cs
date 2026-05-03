using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;
using TeamTrackr.Auth;
using TeamTrackr.Models;

namespace TeamTrackr.Data;

public class AppDbContext : IdentityDbContext<AppUser>
{
    private readonly int _tenantId;

    public AppDbContext(DbContextOptions<AppDbContext> options, ITenantProvider tenantProvider)
        : base(options)
    {
        _tenantId = tenantProvider.GetCurrentTenantId();
    }

    public DbSet<Tenant> Tenants => Set<Tenant>();
    public DbSet<Project> Projects => Set<Project>();
    public DbSet<TaskItem> TaskItems => Set<TaskItem>();
    public DbSet<TaskLabel> TaskLabels => Set<TaskLabel>();
    public DbSet<TaskItemLabel> TaskItemLabels => Set<TaskItemLabel>();
    public DbSet<Comment> Comments => Set<Comment>();
    public DbSet<Subscription> Subscriptions => Set<Subscription>();
    public DbSet<TenantInvitation> TenantInvitations => Set<TenantInvitation>();

    protected override void OnModelCreating(ModelBuilder builder)
    {
        base.OnModelCreating(builder);

        // Tenant
        builder.Entity<Tenant>(e =>
        {
            e.HasIndex(t => t.Slug).IsUnique();
        });

        // AppUser
        builder.Entity<AppUser>(e =>
        {
            e.HasOne(u => u.Tenant)
                .WithMany()
                .HasForeignKey(u => u.TenantId)
                .OnDelete(DeleteBehavior.Restrict);
        });

        // Project
        builder.Entity<Project>(e =>
        {
            e.HasQueryFilter(p => p.TenantId == _tenantId);
            e.HasIndex(p => new { p.TenantId, p.Key }).IsUnique();
        });

        // TaskItem
        builder.Entity<TaskItem>(e =>
        {
            e.HasQueryFilter(t => t.TenantId == _tenantId);
            e.HasOne(t => t.Project)
                .WithMany()
                .HasForeignKey(t => t.ProjectId)
                .OnDelete(DeleteBehavior.Cascade);
            e.HasOne(t => t.Assignee)
                .WithMany()
                .HasForeignKey(t => t.AssigneeId)
                .OnDelete(DeleteBehavior.SetNull);
        });

        // TaskLabel
        builder.Entity<TaskLabel>(e =>
        {
            e.HasQueryFilter(l => l.TenantId == _tenantId);
        });

        // TaskItemLabel (join table)
        builder.Entity<TaskItemLabel>(e =>
        {
            e.HasKey(til => new { til.TaskItemId, til.TaskLabelId });
            e.HasOne(til => til.TaskItem)
                .WithMany(t => t.TaskItemLabels)
                .HasForeignKey(til => til.TaskItemId)
                .OnDelete(DeleteBehavior.Cascade);
            e.HasOne(til => til.TaskLabel)
                .WithMany(l => l.TaskItemLabels)
                .HasForeignKey(til => til.TaskLabelId)
                .OnDelete(DeleteBehavior.Cascade);
        });

        // Comment
        builder.Entity<Comment>(e =>
        {
            e.HasQueryFilter(c => c.TenantId == _tenantId);
            e.HasOne(c => c.TaskItem)
                .WithMany()
                .HasForeignKey(c => c.TaskItemId)
                .OnDelete(DeleteBehavior.Cascade);
            e.HasOne(c => c.Author)
                .WithMany()
                .HasForeignKey(c => c.AuthorId)
                .OnDelete(DeleteBehavior.Restrict);
        });

        // Subscription
        builder.Entity<Subscription>(e =>
        {
            e.HasOne(s => s.Tenant)
                .WithMany()
                .HasForeignKey(s => s.TenantId)
                .OnDelete(DeleteBehavior.Cascade);
            e.HasIndex(s => s.TenantId);
        });

        // TenantInvitation
        builder.Entity<TenantInvitation>(e =>
        {
            e.HasIndex(i => i.Token).IsUnique();
            e.HasIndex(i => i.TenantId);
            e.HasOne(i => i.Tenant)
                .WithMany()
                .HasForeignKey(i => i.TenantId)
                .OnDelete(DeleteBehavior.Cascade);
            e.HasOne(i => i.InvitedBy)
                .WithMany()
                .HasForeignKey(i => i.InvitedByUserId)
                .OnDelete(DeleteBehavior.Restrict);
        });

        // Seed default tenant
        builder.Entity<Tenant>().HasData(new Tenant
        {
            Id = 1,
            Name = "Default Organization",
            Slug = "default",
            Plan = "free",
            CreatedAt = new DateTime(2025, 1, 1, 0, 0, 0, DateTimeKind.Utc)
        });
    }
}
