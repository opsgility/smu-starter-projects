using Xunit;

namespace Halcyon.Adventure.Data.Tests.Sales;

// Three convention tests that prove the partial-class overrides from Lesson 2 Exercise 5
// landed correctly. All three stay skipped until Exercise 5 removes the Skip arguments.
// The test bodies reference types that only exist after the scaffold + partial-class work
// completes.

public class SalesConventionsTest
{
    [Fact(Skip = "Lesson 2 Exercise 5 unlocks this once AdventureWorksSalesContext.Partial.cs lands.")]
    public void Money_Columns_Have_Precision_Configured()
    {
        // After Exercise 5, inspect ctx.Model and assert that
        // SalesOrderHeader.TotalDue + .SubTotal + .TaxAmt + .Freight all carry
        // precision 19 scale 4. Same for SalesOrderDetail.UnitPrice +
        // .UnitPriceDiscount + .LineTotal.
    }

    [Fact(Skip = "Lesson 2 Exercise 5 unlocks this once the soft-delete global filter lands.")]
    public void Customer_Soft_Delete_Filter_Hides_Null_ModifiedDate()
    {
        // After Exercise 5, insert a Customer with ModifiedDate = null, then
        // assert default ctx.Customer.ToListAsync() does NOT return it, and
        // ctx.Customer.IgnoreQueryFilters().ToListAsync() DOES return it.
    }

    [Fact(Skip = "Lesson 2 Exercise 5 unlocks this once Customer.Partial.cs lands IsPlatinum.")]
    public void Customer_IsPlatinum_Reflects_StoreId()
    {
        // After Exercise 5, assert the IsPlatinum computed property reads from
        // StoreID.HasValue — true for store customers, false for individuals.
    }
}
