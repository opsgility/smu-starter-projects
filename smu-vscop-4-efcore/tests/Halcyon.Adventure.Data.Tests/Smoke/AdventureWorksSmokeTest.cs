using Microsoft.Data.SqlClient;
using Xunit;

namespace Halcyon.Adventure.Data.Tests.Smoke;

// Proves the local SQL Server + AdventureWorks2025 database is reachable from the
// test host — a one-liner smoke test that catches a bad VM image before the student
// spends 20 minutes thinking EF Core is broken.
public class AdventureWorksSmokeTest
{
    private const string ConnectionString =
        "Server=.;Database=AdventureWorks2025;Trusted_Connection=True;TrustServerCertificate=True";

    [Fact]
    public void Can_Open_SqlConnection_To_Local_AdventureWorks2025()
    {
        using var connection = new SqlConnection(ConnectionString);
        connection.Open();

        using var command = connection.CreateCommand();
        command.CommandText = "SELECT TOP 1 CustomerID FROM Sales.Customer";
        var firstCustomerId = (int)command.ExecuteScalar()!;

        Assert.True(firstCustomerId > 0, "Sales.Customer should contain at least one row with a positive CustomerID.");
    }
}
