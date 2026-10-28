using Halcyon.Adventure.Data.Generated;
using Microsoft.EntityFrameworkCore;

namespace Halcyon.Adventure.Data.Reporting;

/// <summary>
/// Produces the Top-N "Platinum" (store) customer report with their full order
/// history. Deliberately shipped as an N+1 — Lesson 4 Exercise 4 rewrites the
/// method body to a single eager-loaded + split-query + projected call.
/// </summary>
public class CustomerSalesReportService
{
    private readonly AdventureWorksSalesContext _context;

    public CustomerSalesReportService(AdventureWorksSalesContext context)
    {
        _context = context;
    }

    public async Task<List<CustomerWithOrdersDto>> GetTopPlatinumWithOrdersAsync(int top)
    {
        var topCustomers = await _context.Customer
            .Where(c => c.StoreID != null)
            .OrderByDescending(c => c.SalesOrderHeader.Count)
            .Take(top)
            .ToListAsync();

        var result = new List<CustomerWithOrdersDto>();

        // N+1 — one SELECT per customer. Lesson 4 teaches finding and fixing this.
        foreach (var customer in topCustomers)
        {
            var orders = await _context.SalesOrderHeader
                .Where(o => o.CustomerID == customer.CustomerID)
                .Include(o => o.SalesOrderDetail)
                .OrderByDescending(o => o.OrderDate)
                .ToListAsync();

            var orderSummaries = orders
                .Select(o => new OrderSummaryDto(
                    o.SalesOrderID,
                    o.OrderDate,
                    o.TotalDue,
                    o.SalesOrderDetail
                        .Select(d => new OrderLineDto(d.ProductID, d.OrderQty, d.LineTotal))
                        .ToList()))
                .ToList();

            result.Add(new CustomerWithOrdersDto(
                customer.CustomerID,
                customer.Store?.Name,
                customer.ModifiedDate,
                orderSummaries));
        }

        return result;
    }
}
