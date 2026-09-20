using ECommerceApi.Models;
using ECommerceApi.Repositories;

namespace ECommerceApi.Services;

public class ProductService : IProductService
{
    private readonly IProductRepository _repository;

    public ProductService(IProductRepository repository)
    {
        _repository = repository;
    }

    public IEnumerable<Product> GetAll() => _repository.GetAll();

    public Product? GetById(int id) => _repository.GetById(id);

    public Product Create(Product product) => _repository.Create(product);

    public Product? Update(Product product) => _repository.Update(product);

    public bool Delete(int id) => _repository.Delete(id);

    public IEnumerable<Product> GetByCategory(string category) =>
        _repository.GetAll().Where(p => p.Category.Equals(category, StringComparison.OrdinalIgnoreCase));

    public IEnumerable<Product> SearchByName(string name) =>
        _repository.GetAll().Where(p => p.Name.Contains(name, StringComparison.OrdinalIgnoreCase));
}
