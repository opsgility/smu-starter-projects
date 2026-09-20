// ==============================================
// DataForge Inventory Management System
// ==============================================
// CAPSTONE PROJECT
//
// Build a complete inventory management data layer using EF Core.
//
// Required Entities:
// - Product (Id, Name, SKU, Price, StockQuantity, CategoryId, SupplierId, IsActive, concurrency)
// - Category (Id, Name, Description)
// - Supplier (Id, CompanyName, ContactEmail, Phone)
// - StockMovement (Id, ProductId, Quantity, MovementType [In/Out], Notes, CreatedAt)
//
// Requirements:
// 1. Configure relationships with Fluent API
// 2. Create and apply migrations with seed data
// 3. Implement CRUD for all entities
// 4. Build LINQ reports: products by category, low stock, movement history, supplier counts
// 5. Handle concurrency conflicts (UseXminAsConcurrencyToken)
// 6. Add global query filter for soft-delete (IsActive)
// 7. Optimize with Include, AsNoTracking, projections
//
// When done, ask the left-side assistant to "review my code"!
// ==============================================

Console.WriteLine("=== DataForge Inventory Management System ===");
Console.WriteLine("Start building your data layer. Good luck!");
