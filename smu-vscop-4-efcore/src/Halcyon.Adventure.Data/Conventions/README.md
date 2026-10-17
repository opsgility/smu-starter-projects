# Conventions/

Halcyon's convention overrides for the scaffolded EF Core model. Every file here is a `partial class` extension of a generated type in `../Generated/`. The folder-split pattern is what makes `dotnet ef dbcontext scaffold --force` safe to re-run — the generated files get overwritten, these files do not.

Lesson 2 Exercise 5 adds:
- `AdventureWorksSalesContext.Partial.cs` — `OnModelCreatingPartial` with money-precision + soft-delete filter.
- `Customer.Partial.cs` — the Halcyon `IsPlatinum` computed property.

Lesson 6 Exercise 3 extends:
- `CustomerTier.cs` — the byte-backed CustomerTier enum.
- `Customer.Partial.cs` — adds the Tier + TierAssignedDate + TierAssignedByUserId properties.
- `AdventureWorksSalesContext.Partial.cs` — extends `OnModelCreatingPartial` with the CustomerTier fluent config + check constraint.
