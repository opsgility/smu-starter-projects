using Project.Models;

namespace Project.Repositories;

public class AuthorRepository : IAuthorRepository
{
    private readonly List<Author> _authors;
    private int _nextId = 6;

    public AuthorRepository()
    {
        _authors = new List<Author>
        {
            new Author { Id = 1, Name = "George Orwell", Bio = "English novelist and essayist known for his sharp criticism of political oppression." },
            new Author { Id = 2, Name = "Jane Austen", Bio = "English novelist known for her commentary on the British landed gentry." },
            new Author { Id = 3, Name = "Mark Twain", Bio = "American writer and humorist, called the father of American literature." },
            new Author { Id = 4, Name = "Gabriel Garcia Marquez", Bio = "Colombian novelist and Nobel Prize laureate, pioneer of magical realism." },
            new Author { Id = 5, Name = "Haruki Murakami", Bio = "Japanese writer whose works blend surrealism with everyday life." }
        };
    }

    public List<Author> GetAll() => _authors.ToList();

    public Author? GetById(int id) => _authors.FirstOrDefault(a => a.Id == id);

    public Author Create(Author author)
    {
        author.Id = _nextId++;
        _authors.Add(author);
        return author;
    }

    public Author? Update(int id, Author author)
    {
        var existing = _authors.FirstOrDefault(a => a.Id == id);
        if (existing == null) return null;

        existing.Name = author.Name;
        existing.Bio = author.Bio;
        return existing;
    }

    public bool Delete(int id)
    {
        var author = _authors.FirstOrDefault(a => a.Id == id);
        if (author == null) return false;
        _authors.Remove(author);
        return true;
    }
}
