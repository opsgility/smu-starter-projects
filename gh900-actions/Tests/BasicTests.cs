using Xunit;

namespace CloudNest.Tests;

public class BasicTests
{
    [Fact]
    public void Greeter_SayHello_ReturnsExpectedMessage()
    {
        var result = Greeter.SayHello("GitHub");
        Assert.Equal("Hello, GitHub!", result);
    }
}
