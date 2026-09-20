package com.skillmeup.inventory;

import java.util.List;
import java.util.Map;
import java.util.DoubleSummaryStatistics;
import java.util.stream.Collectors;

public class ReportService {

    // TODO Exercise 1: Implement getLowStockProducts(List<Product> products, int threshold)
    // Use: products.stream().filter(p -> p.getQuantity() < threshold).collect(Collectors.toList())
    public List<Product> getLowStockProducts(List<Product> products, int threshold) {
        return List.of(); // TODO: replace with stream filter
    }

    // TODO Exercise 2: Implement groupByCategory(List<Product> products)
    // Use: products.stream().collect(Collectors.groupingBy(Product::getCategory))
    // Returns Map<String, List<Product>>
    public Map<String, List<Product>> groupByCategory(List<Product> products) {
        return Map.of(); // TODO: replace with Collectors.groupingBy
    }

    // TODO Exercise 3: Implement getPriceStatsByCategory(List<Product> products)
    // Use: Collectors.groupingBy(Product::getCategory, Collectors.summarizingDouble(Product::getUnitPrice))
    // Returns Map<String, DoubleSummaryStatistics>
    public Map<String, DoubleSummaryStatistics> getPriceStatsByCategory(List<Product> products) {
        return Map.of(); // TODO: replace with Collectors.groupingBy + summarizingDouble
    }
}
