using Project.Models;

namespace Project.Repositories;

public interface IBookRepository
{
    List<Book> GetAll();
    Book? GetById(int id);
    Book Create(Book book);
    Book? Update(Book book);
    bool Delete(int id);
    List<Book> SearchByTitle(string term);
}
