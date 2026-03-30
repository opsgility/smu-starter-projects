namespace CloudNest;

class Program
{
    static void Main(string[] args)
    {
        Console.WriteLine("CloudNest Calculator");
        Console.WriteLine("====================");

        var calc = new Calculator();

        Console.WriteLine($"2 + 3 = {calc.Add(2, 3)}");
        Console.WriteLine($"10 - 4 = {calc.Subtract(10, 4)}");
    }
}
