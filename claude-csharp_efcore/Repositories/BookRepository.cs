using Project.Models;

namespace Project.Repositories;

public class BookRepository : IBookRepository
{
    private readonly List<Book> _books;
    private int _nextId = 6;

    public BookRepository()
    {
        _books = new List<Book>
        {
            new Book { Id = 1, Title = "1984", AuthorId = 1, ISBN = "978-0451524935", PublicationYear = 1949 },
            new Book { Id = 2, Title = "Pride and Prejudice", AuthorId = 2, ISBN = "978-0141439518", PublicationYear = 1813 },
            new Book { Id = 3, Title = "The Adventures of Tom Sawyer", AuthorId = 3, ISBN = "978-0143039563", PublicationYear = 1876 },
            new Book { Id = 4, Title = "One Hundred Years of Solitude", AuthorId = 4, ISBN = "978-0060883287", PublicationYear = 1967 },
            new Book { Id = 5, Title = "Norwegian Wood", AuthorId = 5, ISBN = "978-0375704024", PublicationYear = 1987 }
        };
    }

    public List<Book> GetAll() => _books.ToList();

    public Book? GetById(int id) => _books.FirstOrDefault(b => b.Id == id);

    public Book Create(Book book)
    {
        book.Id = _nextId++;
        _books.Add(book);
        return book;
    }

    public Book? Update(int id, Book book)
    {
        var existing = _books.FirstOrDefault(b => b.Id == id);
        if (existing == null) return null;

        existing.Title = book.Title;
        existing.AuthorId = book.AuthorId;
        existing.ISBN = book.ISBN;
        existing.PublicationYear = book.PublicationYear;
        return existing;
    }

    public bool Delete(int id)
    {
        var book = _books.FirstOrDefault(b => b.Id == id);
        if (book == null) return false;
        _books.Remove(book);
        return true;
    }

    public List<Book> SearchByTitle(string title) =>
        _books.Where(b => b.Title.Contains(title, StringComparison.OrdinalIgnoreCase)).ToList();
}
