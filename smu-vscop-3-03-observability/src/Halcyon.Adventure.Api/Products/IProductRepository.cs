namespace Halcyon.Adventure.Api.Products;

/// <summary>
/// Thin storage abstraction. The in-memory implementation (ProductRepository)
/// keeps the lab self-contained; a later course wires the real
/// AdventureWorks DbContext behind the same interface.
/// </summary>
public interface IProductRepository
{
    IReadOnlyCollection<Product> GetAll();

    bool TryGet(int id, out Product? product);

    Product Create(CreateProductRequest request);

    Product Update(int id, UpdateProductRequest request);

    bool Delete(int id);
}
