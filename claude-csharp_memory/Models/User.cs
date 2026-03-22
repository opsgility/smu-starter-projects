namespace MemoryApp.Models;

// No XML docs (inconsistent with Order.cs)
public class User
{
    public int id { get; set; }        // wrong casing!
    public string name { get; set; } = string.Empty;  // wrong casing!
    public string email { get; set; } = string.Empty;  // wrong casing!
}
