# az-dev-130-ef-core

EF Core 9 starter for Anchorline's order model.

## Entities

- `Customer` (unique on `Email`)
- `Product` (unique on `Sku`)
- `Order` (index on `PlacedUtc`)
- `OrderLine`

## Env

- `ANCHORLINE_SQL_SERVER` — FQDN of the SQL server (from Module 1).
- `ANCHORLINE_SQL_DATABASE` — default `AnchorlineOrders`.

## Modes

```
dotnet run --project . -- seed   # write baseline customers/products/order
dotnet run --project . -- list   # AsNoTracking + AsSplitQuery read of Orders
dotnet run --project . -- hot    # compare compiled query vs LINQ query on a hot loop
```

## Migrations workflow

```
dotnet ef migrations add InitialCreate
dotnet ef database update            # dev only
dotnet ef migrations add AddOrderPlacedIndex
dotnet ef migrations script InitialCreate AddOrderPlacedIndex -o migration.sql --idempotent
```
