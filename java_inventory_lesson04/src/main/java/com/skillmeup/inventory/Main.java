package com.skillmeup.inventory;

import java.util.Scanner;

public class Main {
    static Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
        // Array-based catalog (from lesson02) — still present for comparison
        Product[] oldCatalog = {
            new Product("P001", "Widget A",    "Electronics", 50,  9.99),
            new Product("P002", "Gadget B",    "Electronics", 20, 24.99),
            new Product("P003", "Sprocket C",  "Hardware",   100,  2.49),
        };
        System.out.println("Old array catalog size: " + oldCatalog.length);

        // New ArrayList-backed store
        InventoryStore store = new InventoryStore();
        store.addProduct(new Product("P001", "Widget A",   "Electronics", 50,  9.99));
        store.addProduct(new Product("P002", "Gadget B",   "Electronics", 20, 24.99));
        store.addProduct(new Product("P003", "Sprocket C", "Hardware",   100,  2.49));

        System.out.println("\nInventory (ArrayList):");
        store.listAll().forEach(System.out::println);

        System.out.print("\nRemove product ID: ");
        String id = scanner.nextLine();
        store.removeProduct(id);
        System.out.println("After removal:");
        store.listAll().forEach(System.out::println);

        scanner.close();
    }
}
