package com.skillmeup.inventory;

public class Main {
    public static void main(String[] args) {
        InventoryStore store = new InventoryStore();
        store.addProduct(new Product("P003", "Sprocket C", "Hardware",   100,  2.49));
        store.addProduct(new Product("P001", "Widget A",   "Electronics", 50,  9.99));
        store.addProduct(new Product("P002", "Gadget B",   "Electronics", 20, 24.99));
        store.addProduct(new Product("P004", "Doohickey",  "Hardware",     5, 14.99));

        System.out.println("Unsorted:"); store.listAll().forEach(System.out::println);
        System.out.println("\nBy name:"); store.sortByName().forEach(System.out::println);
        System.out.println("\nBy price:"); store.sortByPrice().forEach(System.out::println);
        System.out.println("\nBy quantity:"); store.sortByQuantity().forEach(System.out::println);
    }
}
