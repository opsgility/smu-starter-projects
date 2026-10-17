using Xunit;

namespace Halcyon.Adventure.Data.Tests.Sales;

// This test proves the Lesson 2 Exercise 3 scaffold produced a working context
// against AdventureWorks2025. It stays skipped until the scaffold runs — the
// AdventureWorksSalesContext class doesn't exist in the starter so the file
// wouldn't compile with the test unskipped.
//
// Lesson 2 Exercise 3 Task 4 removes the Skip argument.

public class SalesSmokeTest
{
    [Fact(Skip = "Lesson 2 Exercise 3 unlocks this once the DbContext is scaffolded.")]
    public async Task AdventureWorksSalesContext_Returns_Top_Platinum_Customers()
    {
        // After Exercise 3 scaffolds, uncomment the following:
        //
        // using var factory = new AdventureWorksSalesContextFactory();
        // await using var ctx = factory.CreateDbContext(System.Array.Empty<string>());
        // var top5 = await ctx.Customer
        //     .Where(c => c.StoreID != null)
        //     .Take(5)
        //     .ToListAsync();
        // Assert.Equal(5, top5.Count);
        await Task.CompletedTask;
    }
}
