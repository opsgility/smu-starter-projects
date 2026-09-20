using System.Collections.Concurrent;

namespace Anchorline.Functions.RestApi;

public record Todo(int Id, string Title, bool Done, DateTimeOffset Created);
public record TodoCreateDto(string Title);
public record TodoUpdateDto(string Title, bool Done);

public interface ITodoRepository
{
    IEnumerable<Todo> All();
    Todo? Find(int id);
    Todo Add(TodoCreateDto dto);
    Todo? Update(int id, TodoUpdateDto dto);
    bool Delete(int id);
}

public class InMemoryTodoRepository : ITodoRepository
{
    private readonly ConcurrentDictionary<int, Todo> _store = new();
    private int _nextId = 0;

    public InMemoryTodoRepository()
    {
        // Seed a couple so /todos isn't empty on first hit
        Add(new TodoCreateDto("Check inventory for the fall sale"));
        Add(new TodoCreateDto("Call warehouse about the tent shipment"));
    }

    public IEnumerable<Todo> All() => _store.Values.OrderBy(t => t.Id);

    public Todo? Find(int id) => _store.TryGetValue(id, out var t) ? t : null;

    public Todo Add(TodoCreateDto dto)
    {
        var id = Interlocked.Increment(ref _nextId);
        var todo = new Todo(id, dto.Title, false, DateTimeOffset.UtcNow);
        _store[id] = todo;
        return todo;
    }

    public Todo? Update(int id, TodoUpdateDto dto)
    {
        if (!_store.ContainsKey(id)) return null;
        var updated = new Todo(id, dto.Title, dto.Done, _store[id].Created);
        _store[id] = updated;
        return updated;
    }

    public bool Delete(int id) => _store.TryRemove(id, out _);
}
