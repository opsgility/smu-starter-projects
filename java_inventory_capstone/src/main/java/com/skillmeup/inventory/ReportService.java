package com.skillmeup.inventory;

import java.util.ArrayList;
import java.util.DoubleSummaryStatistics;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class ReportService {

    // TODO Capstone Exercise 2: Implement getLowStockAlerts(List<Product> products, int threshold)
    // Create a StockAlert for each product where quantity < threshold.
    // Return the list of triggered alerts.
    public List<StockAlert> getLowStockAlerts(List<Product> products, int threshold) {
        return new ArrayList<>(); // TODO: implement
    }

    // TODO Capstone Exercise 3: Implement generateCategorySummary(List<Product> products)
    // Group by category, then for each category compute:
    //   count of products, total value (sum of quantity * unitPrice), average price
    // Print a formatted summary table. Use streams and Collectors.groupingBy.
    public void generateCategorySummary(List<Product> products) {
        // TODO: implement category summary report
        System.out.println("(not yet implemented)");
    }

    // These are pre-implemented helpers for InventoryManager in Exercise 3:
    public double getTotalInventoryValue(List<Product> products) {
        return products.stream()
                       .mapToDouble(p -> p.getQuantity() * p.getUnitPrice())
                       .sum();
    }

    public double getAveragePrice(List<Product> products) {
        return products.stream()
                       .mapToDouble(Product::getUnitPrice)
                       .average()
                       .orElse(0.0);
    }

    public Map<String, List<Product>> groupByCategory(List<Product> products) {
        return products.stream().collect(Collectors.groupingBy(Product::getCategory));
    }

    public Map<String, DoubleSummaryStatistics> getPriceStatsByCategory(List<Product> products) {
        return products.stream().collect(
            Collectors.groupingBy(Product::getCategory, Collectors.summarizingDouble(Product::getUnitPrice)));
    }
}
