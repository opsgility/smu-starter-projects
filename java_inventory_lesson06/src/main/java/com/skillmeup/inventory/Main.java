package com.skillmeup.inventory;

public class Main {
    public static void main(String[] args) {
        InventoryStore store = new InventoryStore();
        store.addProduct(new Product("P001", "Widget A",   "ELEC", 50,  9.99));
        store.addProduct(new Product("P002", "Gadget B",   "ELEC", 20, 24.99));
        store.addProduct(new Product("P003", "Sprocket C", "HW",  100,  2.49));

        CategoryMap catMap = new CategoryMap();
        catMap.addCategory(new Category("ELEC", "Electronics", "Electronic components"));
        catMap.addCategory(new Category("HW",   "Hardware",    "Hardware supplies"));

        System.out.println("All products:");
        store.listAll().forEach(System.out::println);

        System.out.println("\nCategories:");
        // TODO: call catMap methods to list all categories and their tags
    }
}
