package com.skillmeup.inventory;

public class Main {
    // Sample catalog using a fixed-size array
    static final int MAX_PRODUCTS = 100;
    static Product[] catalog = new Product[MAX_PRODUCTS];
    static int productCount = 0;

    public static void main(String[] args) {
        // Pre-load some products
        catalog[productCount++] = new Product("P001", "Widget A",    "Electronics", 50,  9.99);
        catalog[productCount++] = new Product("P002", "Gadget B",    "Electronics", 20, 24.99);
        catalog[productCount++] = new Product("P003", "Sprocket C",  "Hardware",    100,  2.49);
        catalog[productCount++] = new Product("P004", "Doohickey D", "Hardware",     5, 14.99);

        // TODO Exercise 1: Write a for loop (index-based) to print every product in the array.
        // Stop at productCount, not catalog.length. Print: "1. " + product.toString()

        // TODO Exercise 2: Write a for-each loop over catalog to count and print
        // how many products have quantity < 10. (Watch for null slots!)
        // Print: "Low stock items: N"

        // TODO Exercise 3: Implement a linear search method findByName(String name)
        // below main, then call it from here. Search for "Gadget B" and print the result.
    }

    // TODO Exercise 3 helper: implement this method
    public static Product findByName(String name) {
        // Loop through catalog[0..productCount-1], return product if name matches (case-insensitive)
        return null; // replace with your implementation
    }
}
