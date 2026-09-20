using ECommerceApi.Models;

namespace ECommerceApi.Repositories;

public interface IProductRepository
{
    IEnumerable<Product> GetAll();
    Product? GetById(int id);
    Product Create(Product product);
    Product? Update(Product product);
    bool Delete(int id);
}
