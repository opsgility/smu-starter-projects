using Microsoft.EntityFrameworkCore;
using BrightShelf.Data;
using BrightShelf.Models;

namespace BrightShelf.Services;

public interface IProductService
{
    Task<List<Product>> GetAllProductsAsync();
    Task<Product?> GetProductByIdAsync(int id);
    Task<List<Product>> GetProductsByCategoryAsync(string category);
}

public class ProductService : IProductService
{
    private readonly AppDbContext _context;
    private readonly ILogger<ProductService> _logger;

    public ProductService(AppDbContext context, ILogger<ProductService> logger)
    {
        _context = context;
        _logger = logger;
    }

    public async Task<List<Product>> GetAllProductsAsync()
    {
        _logger.LogInformation("Fetching all products from database...");

        // Simulate a slow database query so caching improvement is visible
        Thread.Sleep(2000);

        return await _context.Products.ToListAsync();
    }

    public async Task<Product?> GetProductByIdAsync(int id)
    {
        _logger.LogInformation("Fetching product {Id} from database...", id);

        // Simulate slow query
        Thread.Sleep(1000);

        return await _context.Products.FindAsync(id);
    }

    public async Task<List<Product>> GetProductsByCategoryAsync(string category)
    {
        _logger.LogInformation("Fetching products in category {Category} from database...", category);

        // Simulate slow query
        Thread.Sleep(1500);

        return await _context.Products
            .Where(p => p.Category!.Name == category)
            .ToListAsync();
    }
}
