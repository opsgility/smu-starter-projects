# Inventory Management System Requirements

## Entities
- **Product**: Id (int), Name (string), SKU (string, unique), Price (decimal), Category (Category ref), StockQuantity (int), ReorderLevel (int), IsActive (bool)
- **Category**: Id (int), Name (string), Description (string), Products (collection)
- **Supplier**: Id (int), CompanyName (string), ContactEmail (string), Phone (string)
- **PurchaseOrder**: Id (int), Supplier (ref), OrderDate (DateTime), Status (enum: Pending, Approved, Received, Cancelled), Items (collection)
- **PurchaseOrderItem**: Id (int), PurchaseOrder (ref), Product (ref), Quantity (int), UnitPrice (decimal)

## Business Rules
- Products below ReorderLevel should be flagged for reorder
- PurchaseOrder total = sum of (Quantity * UnitPrice) for all items
- SKU must be unique across all products
- Inactive products cannot be added to purchase orders
- A Category can have many Products; a Product belongs to one Category
- A Supplier can have many PurchaseOrders
- When a PurchaseOrder status changes to Received, update Product stock quantities

## Expected Methods
- Product.NeedsReorder() -> bool
- PurchaseOrder.CalculateTotal() -> decimal
- PurchaseOrder.AddItem(product, quantity, unitPrice) -> validates product is active
- Category.GetActiveProducts() -> filtered list
