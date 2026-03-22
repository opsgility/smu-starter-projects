namespace CalculatorApp;

public class Calculator
{
    public double Add(double a, double b) => a + b;
    public double Subtract(double a, double b) => a - b;
    public double Multiply(double a, double b) => a * b;

    public double Divide(double a, double b)
    {
        // Bug: no check for division by zero — students will fix this
        return a / b;
    }
}
