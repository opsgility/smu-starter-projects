// ============================================================
// BrightShelf Capstone Project
// ============================================================
// Build a complete product management web application using
// ASP.NET Core Razor Pages. This capstone combines all skills
// from the course.
//
// REQUIREMENTS:
// ------------------------------------------------------------
//
// 1. DATA LAYER
//    - Create Models (Product with Name, Description, Price, StockQuantity, ImagePath, Category, CreatedAt)
//    - Create AppDbContext inheriting from IdentityDbContext
//    - Configure PostgreSQL connection (database: brightshelf_capstone)
//    - Seed at least 5 sample products
//
// 2. AUTHENTICATION & AUTHORIZATION
//    - Configure ASP.NET Core Identity
//    - Register and Login pages (scaffold or custom)
//    - Protect product management pages with [Authorize]
//    - Allow anonymous access to product listing (read-only)
//
// 3. CRUD OPERATIONS
//    - Products: Index (list), Create, Edit, Details, Delete
//    - File upload for product images (store in wwwroot/uploads/)
//    - Forms with proper validation
//
// 4. API INTEGRATION
//    - Create a typed HttpClient service
//    - Consume at least one external or internal API endpoint
//    - Display API data on a Razor Page
//
// 5. AJAX & INTERACTIVITY
//    - Add client-side search/filter on the product listing
//    - Implement AJAX delete (no full page reload)
//    - Include anti-forgery token handling in JavaScript
//
// 6. CACHING
//    - Add IMemoryCache for frequently accessed data
//    - Apply [ResponseCache] or OutputCache to appropriate pages
//
// 7. SECURITY HARDENING
//    - Add security headers (X-Content-Type-Options, X-Frame-Options)
//    - Custom error pages (404, 500)
//    - Content Security Policy
//    - HTTPS enforcement with proper HSTS
//
// 8. TESTING
//    - Create a Tests/ project with xUnit + Moq
//    - Write at least 3 unit tests for page models
//    - Write at least 1 integration test
//
// ============================================================

var builder = WebApplication.CreateBuilder(args);

// TODO: Add services here
builder.Services.AddRazorPages();

var app = builder.Build();

if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error");
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();
app.UseRouting();
app.UseAuthorization();

app.MapRazorPages();

app.Run();
