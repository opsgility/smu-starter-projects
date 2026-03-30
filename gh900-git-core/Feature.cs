namespace CloudNest;

/// <summary>
/// Feature class for branching exercises.
/// Students will create branches, make changes here, and merge.
/// </summary>
public class Feature
{
    public string Name { get; set; } = "Base Feature";

    public void Run()
    {
        Console.WriteLine($"Running feature: {Name}");
    }
}
