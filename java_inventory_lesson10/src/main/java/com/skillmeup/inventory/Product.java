package com.skillmeup.inventory;

public class Product implements Comparable<Product> {
    private String id;
    private String name;
    private String category;
    private int    quantity;
    private double unitPrice;

    public Product(String id, String name, String category, int quantity, double unitPrice) {
        this.id = id; this.name = name; this.category = category;
        this.quantity = quantity; this.unitPrice = unitPrice;
    }
    public String getId()        { return id; }
    public String getName()      { return name; }
    public String getCategory()  { return category; }
    public int    getQuantity()  { return quantity; }
    public double getUnitPrice() { return unitPrice; }
    public void   setQuantity(int quantity) { this.quantity = quantity; }

    // TODO Exercise 1: Implement compareTo(Product other) — sort by name alphabetically.
    // return this.name.compareToIgnoreCase(other.name)
    @Override
    public int compareTo(Product other) {
        return 0; // TODO: implement
    }

    @Override
    public String toString() {
        return String.format("[%s] %s | Cat: %s | Qty: %d | $%.2f", id, name, category, quantity, unitPrice);
    }
}
