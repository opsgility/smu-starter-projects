using Xunit;

namespace Halcyon.Adventure.Data.Tests.Reporting;

// Lesson 4 — two tests:
//  (1) Report_For_Top_10_Platinum_Customers_Returns_Expected_Row_Count — the "it returns 10 rows"
//      correctness test. Passes on both the pre-fix N+1 shape AND the post-fix shape.
//  (2) Report_For_Top_10_Platinum_Customers_Completes_Under_500ms — the perf regression test.
//      FAILS on the N+1 shape (reports ~11s elapsed); PASSES after Lesson 4 Exercise 4's rewrite.
//
// Test (1) is unskipped at starter time so Lesson 4 Exercise 2 can run it and see the SQL log.
// Test (2) is skipped until Lesson 4 Exercise 5 unlocks it.

public class CustomerSalesReportTests
{
    [Fact(Skip = "Lesson 4 — unlock once the scaffold completes in Lesson 2. Delete the Skip when CustomerSalesReportService compiles.")]
    public async Task Report_For_Top_10_Platinum_Customers_Returns_Expected_Row_Count()
    {
        // After Lesson 2 Exercise 3 scaffolds + CustomerSalesReportService compiles:
        //
        // using var factory = new AdventureWorksSalesContextFactory();
        // await using var ctx = factory.CreateDbContext(System.Array.Empty<string>());
        // var service = new CustomerSalesReportService(ctx);
        // var rows = await service.GetTopPlatinumWithOrdersAsync(top: 10);
        // Assert.Equal(10, rows.Count);
        await Task.CompletedTask;
    }

    [Fact(Skip = "Lesson 4 Exercise 5 unlocks this once the N+1 is fixed. Expected to pass on the Include().ThenInclude().AsSplitQuery() shape; fails on the pre-fix foreach-with-nested-await.")]
    public async Task Report_For_Top_10_Platinum_Customers_Completes_Under_500ms()
    {
        // After Lesson 4 Exercise 4 lands the fix:
        //
        // var sw = Stopwatch.StartNew();
        // var rows = await service.GetTopPlatinumWithOrdersAsync(top: 10);
        // sw.Stop();
        // Assert.True(sw.ElapsedMilliseconds < 500,
        //     $"Report should complete under 500ms; actual = {sw.ElapsedMilliseconds}ms");
        await Task.CompletedTask;
    }
}
