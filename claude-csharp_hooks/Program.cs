using CalculatorApp;

var calc = new Calculator();
Console.WriteLine("Calculator with Hooks");
Console.WriteLine($"2 + 3 = {calc.Add(2, 3)}");
Console.WriteLine($"10 / 3 = {calc.Divide(10, 3):F2}");
