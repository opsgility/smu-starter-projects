using MemoryApp.Models;

namespace MemoryApp;

// Uses var everywhere, no underscore prefix, no XML docs, throws generic Exception
public class UserService
{
    private List<User> users = new();
    private int nextId = 1;

    public User Create(string name, string email)
    {
        var user = new User { id = nextId++, name = name, email = email };
        users.Add(user);
        return user;
    }

    public User GetById(int id)
    {
        var user = users.FirstOrDefault(u => u.id == id);
        if (user == null) throw new Exception("User not found");
        return user;
    }

    public List<User> GetAll()
    {
        var allUsers = users.ToList();
        return allUsers;
    }
}
