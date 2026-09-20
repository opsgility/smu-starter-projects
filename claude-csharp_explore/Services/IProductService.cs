using ECommerceApi.Models;

namespace ECommerceApi.Services;

public interface IProductService
{
    IEnumerable<Product> GetAll();
    Product? GetById(int id);
    Product Create(Product product);
    Product? Update(Product product);
    bool Delete(int id);
    IEnumerable<Product> GetByCategory(string category);
    IEnumerable<Product> SearchByName(string name);
}
