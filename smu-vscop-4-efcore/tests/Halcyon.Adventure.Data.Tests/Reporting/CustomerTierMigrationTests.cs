using Xunit;

namespace Halcyon.Adventure.Data.Tests.Reporting;

// Lesson 6 — four tests that come online progressively as the exercises land their artifacts.
//
// Exercise 3 unlocks test (1).
// Exercise 4 unlocks tests (2), (3), (4) after `dotnet ef database update` applies.
//
// The tests reference types + behaviors that only exist after the respective exercises run,
// so each test stays skipped until its exercise is complete.

public class CustomerTierMigrationTests
{
    [Fact(Skip = "Lesson 6 Exercise 3 unlocks this once the partial-class config lands.")]
    public void CustomerTier_HasConversion_To_Byte()
    {
        // After Exercise 3, read the EF Core model metadata and assert the Tier property
        // carries HasConversion<byte>() + HasColumnType("tinyint") + HasDefaultValue(Standard)
        // + IsRequired() per the design doc in docs/data-decisions/add-customer-tier.md.
    }

    [Fact(Skip = "Lesson 6 Exercise 4 unlocks this once the AddCustomerTier migration applies to the live DB.")]
    public async Task Migration_Up_Adds_Tier_Column_To_Sales_Customer()
    {
        // After Exercise 4, query INFORMATION_SCHEMA.COLUMNS and assert the three new columns
        // (Tier tinyint NOT NULL, TierAssignedDate datetime2(3) NULL, TierAssignedByUserId int NULL)
        // exist on Sales.Customer.
        await Task.CompletedTask;
    }

    [Fact(Skip = "Lesson 6 Exercise 4 unlocks this once the check constraint is in the DB.")]
    public async Task Migration_Up_Adds_Check_Constraint()
    {
        // After Exercise 4, query sys.check_constraints and assert CK_Customer_Tier exists
        // with definition that enforces Tier IN (0, 1, 2, 3).
        await Task.CompletedTask;
    }

    [Fact(Skip = "Lesson 6 Exercise 4 unlocks this once the migration applies.")]
    public async Task Can_Round_Trip_Platinum_Tier()
    {
        // After Exercise 4, insert a Customer with Tier = Platinum, read it back,
        // assert Tier == Platinum.
        await Task.CompletedTask;
    }
}
