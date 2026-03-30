using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using BrightShelf.Data;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddRazorPages();

builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql(builder.Configuration.GetConnectionString("DefaultConnection")));

builder.Services.AddDefaultIdentity<IdentityUser>(options =>
{
    options.SignIn.RequireConfirmedAccount = false;
})
.AddEntityFrameworkStores<AppDbContext>();

var app = builder.Build();

// TODO: Students will add security hardening here:
// - Custom error pages (UseStatusCodePagesWithReExecute)
// - Security headers middleware (X-Content-Type-Options, X-Frame-Options, etc.)
// - HTTPS redirection is already present but students review HSTS settings
// - Content Security Policy headers

if (!app.Environment.IsDevelopment())
{
    // Uses default exception handling - students will add custom error pages
    app.UseExceptionHandler("/Error");
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();
app.UseRouting();

app.UseAuthentication();
app.UseAuthorization();

// TODO: Students will add page-level authorization filters
// TODO: Students will add rate limiting
// TODO: Students will add CORS policy if needed

app.MapRazorPages();

using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    db.Database.EnsureCreated();
}

app.Run();
