using CalculatorApp;

var calc = new Calculator();
Console.WriteLine("Calculator App");
Console.WriteLine($"10 + 5 = {calc.Add(10, 5)}");
Console.WriteLine($"10 - 5 = {calc.Subtract(10, 5)}");
Console.WriteLine($"10 * 5 = {calc.Multiply(10, 5)}");
Console.WriteLine($"10 / 5 = {calc.Divide(10, 5)}");
