using Project.Models;

namespace Project.Repositories;

public interface IAuthorRepository
{
    List<Author> GetAll();
    Author? GetById(int id);
    Author Create(Author author);
    Author? Update(int id, Author author);
    bool Delete(int id);
}
