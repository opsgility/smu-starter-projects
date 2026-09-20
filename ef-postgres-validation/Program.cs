using DataForge.Data;
using DataForge.Models;
using Microsoft.EntityFrameworkCore;
using System.ComponentModel.DataAnnotations;

Console.WriteLine("=== DataForge Validation & Concurrency ===\n");

using var context = new AppDbContext();
SeedData.Initialize(context);

// ==============================================
// EXERCISE 1: Manual Validation
// ==============================================
// After adding data annotations to the Product model,
// use Validator.TryValidateObject to test validation.

Console.WriteLine("--- Exercise 1: Manual Validation ---");

var invalidProduct = new Product
{
    Name = "",           // Should fail: Required, MinimumLength
    Price = -5.00m,      // Should fail: Range
    StockQuantity = -1,  // Should fail: Range
    CategoryId = 1
};

var validationResults = new List<ValidationResult>();
var validationContext = new ValidationContext(invalidProduct);
bool isValid = Validator.TryValidateObject(invalidProduct, validationContext, validationResults, validateAllProperties: true);

Console.WriteLine($"Is valid: {isValid}");
if (!isValid)
{
    foreach (var error in validationResults)
    {
        Console.WriteLine($"  Error: {error.ErrorMessage}");
    }
}
else
{
    Console.WriteLine("  (No validation errors — have you added annotations to Product.cs yet?)");
}
Console.WriteLine();

// ==============================================
// EXERCISE 2: Saving Invalid Data
// ==============================================
// Try saving an invalid product and catch the exception.
// Note: EF Core does NOT automatically run DataAnnotations validation!
// The database constraints will catch some issues, but not all.

Console.WriteLine("--- Exercise 2: Save Invalid Data ---");

// TODO: Try to save a product with invalid data
// What happens? Does EF Core validate the annotations?
// Try adding manual validation BEFORE saving.

Console.WriteLine();

// ==============================================
// EXERCISE 3: Concurrency - Simulated Conflict
// ==============================================
// Simulate two users editing the same product at the same time.

Console.WriteLine("--- Exercise 3: Concurrency Conflict ---");

// Load the same product in two different contexts
var product1 = context.Products.First();
Console.WriteLine($"Loaded: {product1.Name}, Price: {product1.Price}");

// Simulate another user updating the same product
using (var context2 = new AppDbContext())
{
    var product2 = context2.Products.First(p => p.Id == product1.Id);
    product2.Price = 999.99m;
    context2.SaveChanges();
    Console.WriteLine($"User 2 updated price to: {product2.Price}");
}

// Now try to save from the first context
product1.Price = 1.99m;
try
{
    context.SaveChanges();
    Console.WriteLine("Save succeeded (unexpected!)");
}
catch (DbUpdateConcurrencyException ex)
{
    Console.WriteLine($"Concurrency conflict detected! {ex.Message}");

    // TODO: Handle the conflict
    // Options:
    // a) Client wins: reload and overwrite
    // b) Database wins: reload and discard changes
    // c) Merge: compare values and decide

    // Example - Database wins:
    foreach (var entry in ex.Entries)
    {
        // Reload the entity from database
        await entry.ReloadAsync();
        Console.WriteLine($"Reloaded from database. Current price: {((Product)entry.Entity).Price}");
    }
}
Console.WriteLine();

// ==============================================
// EXERCISE 4: Custom Validation
// ==============================================
// Create a custom validation attribute or implement IValidatableObject
// on the Product class. Ideas:
//   - SKU format validation (if you add a SKU property)
//   - Price must be less than a maximum for certain categories
//   - StockQuantity warning if over a threshold

// TODO: Implement IValidatableObject on Product or create a custom attribute
// Console.WriteLine("--- Exercise 4: Custom Validation ---");

Console.WriteLine();

// ==============================================
// EXERCISE 5: Concurrency Retry Pattern
// ==============================================
// Implement a retry loop that handles concurrency conflicts gracefully.

// TODO: Write a method that:
// 1. Loads a product
// 2. Modifies it
// 3. Tries to save
// 4. On DbUpdateConcurrencyException, reloads and retries (up to 3 times)

// Console.WriteLine("--- Exercise 5: Retry Pattern ---");

Console.WriteLine();

Console.WriteLine("=== Validation & Concurrency Complete ===");
