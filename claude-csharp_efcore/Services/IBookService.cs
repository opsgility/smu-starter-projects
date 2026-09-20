using Project.DTOs;

namespace Project.Services;

public interface IBookService
{
    List<BookResponse> GetAll();
    BookResponse? GetById(int id);
    BookResponse Create(CreateBookRequest request);
    BookResponse? Update(int id, CreateBookRequest request);
    bool Delete(int id);
    List<BookResponse> SearchByTitle(string title);
}
