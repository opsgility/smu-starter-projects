namespace Halcyon.Adventure.Data.Reporting;

// Projection DTOs for the Top-N Platinum customer report.
// Deliberately nested records with no EF-tracked entities so the Lesson 4
// rewrite can project straight into them in a single query without a
// materialize-then-map step.

public record CustomerWithOrdersDto(
    int CustomerId,
    string? StoreName,
    DateTime? CustomerSince,
    IReadOnlyList<OrderSummaryDto> Orders);

public record OrderSummaryDto(
    int SalesOrderId,
    DateTime OrderDate,
    decimal TotalDue,
    IReadOnlyList<OrderLineDto> Lines);

public record OrderLineDto(
    int ProductId,
    short OrderQty,
    decimal LineTotal);
