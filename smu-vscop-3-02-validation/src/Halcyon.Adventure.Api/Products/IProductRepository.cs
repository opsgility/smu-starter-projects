namespace Halcyon.Adventure.Api.Products;

public interface IProductRepository
{
    IReadOnlyList<Product> GetAll();
    Product? Get(int id);
    Product Add(Product product);
    bool Update(int id, Action<Product> mutate);
    bool Delete(int id);
    void Clear();
}
