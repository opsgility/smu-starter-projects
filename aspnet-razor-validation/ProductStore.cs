using BrightShelf.Models;

namespace BrightShelf;

public static class ProductStore
{
    private static int _nextId = 6;

    public static List<Product> Products { get; } = new()
    {
        new() { Id = 1, Name = "The Midnight Library", Author = "Matt Haig",
                Category = "Fiction", Price = 14.99m,
                Description = "Between life and death there is a library." },
        new() { Id = 2, Name = "A Short History of Nearly Everything", Author = "Bill Bryson",
                Category = "Science", Price = 12.99m,
                Description = "A journey through science from the Big Bang to civilization." },
        new() { Id = 3, Name = "Clean Code", Author = "Robert C. Martin",
                Category = "Technology", Price = 29.99m,
                Description = "A handbook of agile software craftsmanship." },
        new() { Id = 4, Name = "Sapiens", Author = "Yuval Noah Harari",
                Category = "History", Price = 16.99m,
                Description = "A brief history of humankind." },
        new() { Id = 5, Name = "Dune", Author = "Frank Herbert",
                Category = "Fiction", Price = 11.99m,
                Description = "A science fiction masterpiece set on the desert planet Arrakis." }
    };

    public static int GetNextId() => _nextId++;

    public static Product? GetById(int id) => Products.FirstOrDefault(p => p.Id == id);

    public static void Update(Product product)
    {
        var existing = GetById(product.Id);
        if (existing != null)
        {
            existing.Name = product.Name;
            existing.Author = product.Author;
            existing.Category = product.Category;
            existing.Price = product.Price;
            existing.Description = product.Description;
        }
    }

    public static void Delete(int id)
    {
        var existing = GetById(id);
        if (existing != null)
            Products.Remove(existing);
    }
}
