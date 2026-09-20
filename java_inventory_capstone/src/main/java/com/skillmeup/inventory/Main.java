package com.skillmeup.inventory;

import java.util.List;

public class Main {
    public static void main(String[] args) {
        InventoryStore store = new InventoryStore();
        store.addProduct(new Product("P001", "Widget A",    "Electronics",  50,   9.99));
        store.addProduct(new Product("P002", "Gadget B",    "Electronics",  20,  24.99));
        store.addProduct(new Product("P003", "Sprocket C",  "Hardware",    100,   2.49));
        store.addProduct(new Product("P004", "Doohickey",   "Hardware",      5,  14.99));
        store.addProduct(new Product("P005", "Thingamajig", "Electronics",   3,  49.99));
        store.addProduct(new Product("P006", "Bolt Pack",   "Hardware",    200,   0.99));
        store.addProduct(new Product("P007", "Sensor X",    "Electronics",   8,  89.99));

        ReportService reports = new ReportService();
        List<Product> all = store.listAll();

        System.out.println("=== Low Stock Alerts (threshold: 10) ===");
        reports.getLowStockAlerts(all, 10).forEach(System.out::println);

        System.out.println("\n=== Category Summary ===");
        reports.generateCategorySummary(all);

        System.out.println("\n=== Price Stats ===");
        reports.getPriceStatsByCategory(all).forEach((cat, stats) ->
            System.out.printf("  %s: count=%d avg=$%.2f%n", cat, stats.getCount(), stats.getAverage()));

        System.out.println("\n=== Sorted by Name ===");
        store.sortByName().forEach(System.out::println);
    }
}
