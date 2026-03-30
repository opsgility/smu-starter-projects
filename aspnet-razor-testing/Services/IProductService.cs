using BrightShelf.Models;

namespace BrightShelf.Services;

public interface IProductService
{
    Task<List<Product>> GetAllAsync();
    Task<Product?> GetByIdAsync(int id);
    Task<Product> CreateAsync(Product product);
    Task<Product?> UpdateAsync(Product product);
    Task<bool> DeleteAsync(int id);
}
