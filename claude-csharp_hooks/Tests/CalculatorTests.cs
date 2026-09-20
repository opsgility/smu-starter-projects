using Xunit;
using CalculatorApp;

namespace CalculatorApp.Tests;

public class CalculatorTests
{
    private readonly Calculator _calc = new();

    [Fact] public void Add_TwoNumbers_ReturnsSum() => Assert.Equal(5, _calc.Add(2, 3));
    [Fact] public void Add_NegativeNumbers_ReturnsSum() => Assert.Equal(-1, _calc.Add(2, -3));
    [Fact] public void Subtract_TwoNumbers_ReturnsDifference() => Assert.Equal(7, _calc.Subtract(10, 3));
    [Fact] public void Subtract_NegativeResult() => Assert.Equal(-3, _calc.Subtract(2, 5));
    [Fact] public void Multiply_TwoNumbers_ReturnsProduct() => Assert.Equal(15, _calc.Multiply(3, 5));
    [Fact] public void Multiply_ByZero_ReturnsZero() => Assert.Equal(0, _calc.Multiply(5, 0));
    [Fact] public void Divide_TwoNumbers_ReturnsQuotient() => Assert.Equal(4, _calc.Divide(12, 3));
    [Fact] public void Divide_ByZero_ThrowsException() => Assert.Throws<DivideByZeroException>(() => _calc.Divide(10, 0));
}
