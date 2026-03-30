namespace CloudNest;

class Program
{
    static void Main(string[] args)
    {
        Console.WriteLine("CloudNest - GitHub Actions CI/CD");
        Console.WriteLine("================================");
        Console.WriteLine("Build and test this project with GitHub Actions.");

        var greeting = Greeter.SayHello("World");
        Console.WriteLine(greeting);
    }
}

public static class Greeter
{
    public static string SayHello(string name) => $"Hello, {name}!";
}
