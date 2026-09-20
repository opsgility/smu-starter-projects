using Project.DTOs;
using Project.Models;
using Project.Repositories;

namespace Project.Services;

public class BookService : IBookService
{
    private readonly IBookRepository _bookRepository;
    private readonly IAuthorRepository _authorRepository;

    public BookService(IBookRepository bookRepository, IAuthorRepository authorRepository)
    {
        _bookRepository = bookRepository;
        _authorRepository = authorRepository;
    }

    public List<BookResponse> GetAll()
    {
        var books = _bookRepository.GetAll();
        return books.Select(MapToResponse).ToList();
    }

    public BookResponse? GetById(int id)
    {
        var book = _bookRepository.GetById(id);
        return book == null ? null : MapToResponse(book);
    }

    public BookResponse Create(CreateBookRequest request)
    {
        var book = new Book
        {
            Title = request.Title,
            AuthorId = request.AuthorId,
            ISBN = request.ISBN,
            PublicationYear = request.PublicationYear
        };

        var created = _bookRepository.Create(book);
        return MapToResponse(created);
    }

    public BookResponse? Update(int id, CreateBookRequest request)
    {
        var book = new Book
        {
            Title = request.Title,
            AuthorId = request.AuthorId,
            ISBN = request.ISBN,
            PublicationYear = request.PublicationYear
        };

        var updated = _bookRepository.Update(id, book);
        return updated == null ? null : MapToResponse(updated);
    }

    public bool Delete(int id) => _bookRepository.Delete(id);

    public List<BookResponse> SearchByTitle(string title)
    {
        var books = _bookRepository.SearchByTitle(title);
        return books.Select(MapToResponse).ToList();
    }

    private BookResponse MapToResponse(Book book)
    {
        var author = _authorRepository.GetById(book.AuthorId);
        return new BookResponse
        {
            Id = book.Id,
            Title = book.Title,
            AuthorName = author?.Name ?? "Unknown",
            ISBN = book.ISBN,
            PublicationYear = book.PublicationYear
        };
    }
}
