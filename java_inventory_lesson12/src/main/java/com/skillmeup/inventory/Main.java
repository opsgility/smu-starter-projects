package com.skillmeup.inventory;

import java.util.List;
import java.util.Map;

public class Main {
    public static void main(String[] args) {
        InventoryStore store = new InventoryStore();
        store.addProduct(new Product("P001", "Widget A",   "Electronics", 50,   9.99));
        store.addProduct(new Product("P002", "Gadget B",   "Electronics", 20,  24.99));
        store.addProduct(new Product("P003", "Sprocket C", "Hardware",   100,   2.49));
        store.addProduct(new Product("P004", "Doohickey",  "Hardware",     5,  14.99));
        store.addProduct(new Product("P005", "Thingamajig","Electronics",  3,  49.99));

        ReportService reports = new ReportService();
        List<Product> all = store.listAll();

        System.out.println("=== Low Stock (qty < 10) ===");
        reports.getLowStockProducts(all, 10).forEach(System.out::println);

        System.out.println("\n=== By Category ===");
        Map<String, List<Product>> grouped = reports.groupByCategory(all);
        grouped.forEach((cat, prods) -> {
            System.out.println(cat + ":");
            prods.forEach(p -> System.out.println("  " + p));
        });

        System.out.println("\n=== Price Stats by Category ===");
        reports.getPriceStatsByCategory(all).forEach((cat, stats) ->
            System.out.printf("  %s: count=%d avg=$%.2f min=$%.2f max=$%.2f%n",
                cat, stats.getCount(), stats.getAverage(), stats.getMin(), stats.getMax()));
    }
}
