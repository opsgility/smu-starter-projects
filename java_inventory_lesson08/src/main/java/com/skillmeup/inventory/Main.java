package com.skillmeup.inventory;

public class Main {
    public static void main(String[] args) {
        ProductRepository repo = new ProductRepository();
        repo.save(new Product("P001", "Widget A",   "Electronics", 50,  9.99));
        repo.save(new Product("P002", "Gadget B",   "Electronics", 20, 24.99));
        repo.save(new Product("P003", "Sprocket C", "Hardware",   100,  2.49));

        System.out.println("All products from repository:");
        repo.findAll().forEach(System.out::println);

        System.out.println("\nFind P002: " + repo.findById("P002"));
        System.out.println("Delete P001: " + repo.delete("P001"));
        System.out.println("After delete:");
        repo.findAll().forEach(System.out::println);
    }
}
