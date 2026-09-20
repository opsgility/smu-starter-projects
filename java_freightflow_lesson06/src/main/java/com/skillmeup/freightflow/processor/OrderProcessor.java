package com.skillmeup.freightflow.processor;

import com.skillmeup.freightflow.model.Order;
import com.skillmeup.freightflow.service.NotificationService;
import com.skillmeup.freightflow.service.ProductPricingService;
import org.springframework.stereotype.Component;
import java.math.BigDecimal;
import java.util.*;
import java.util.concurrent.*;

/**
 * Processes orders using CompletableFuture pipelines.
 * Baseline throughput: ~580 orders/sec.
 *
 * TODO Exercise 3: Open OrderRepository.java — replace DriverManager.getConnection() with injected DataSource
 * TODO Exercise 4: Convert the INSERT loop to batch insert using addBatch() / executeBatch()
 * TODO Exercise 5: Run BenchmarkRunner — record before/after insert throughput above
 */
@Component
public class OrderProcessor {
    private final ProductPricingService pricingService;
    private final NotificationService notificationService;
    private final ExecutorService executor;

    public OrderProcessor(ProductPricingService pricingService,
                         NotificationService notificationService) {
        this.pricingService = pricingService;
        this.notificationService = notificationService;
        int threads = Runtime.getRuntime().availableProcessors();
        this.executor = new ThreadPoolExecutor(
            threads, threads * 2,
            60L, TimeUnit.SECONDS,
            new ArrayBlockingQueue<>(500),
            new ThreadPoolExecutor.CallerRunsPolicy()
        );
    }

    public List<ProcessingResult> processAllOrders(List<Order> orders) {
        List<CompletableFuture<ProcessingResult>> futures = orders.stream()
            .map(order -> CompletableFuture
                .supplyAsync(() -> processOrder(order), executor)
                .exceptionally(ex -> ProcessingResult.failed(order.getId(), ex.getMessage())))
            .toList();

        CompletableFuture.allOf(futures.toArray(new CompletableFuture[0])).join();

        return futures.stream()
            .map(CompletableFuture::join)
            .toList();
    }

    private ProcessingResult processOrder(Order order) {
        try {
            BigDecimal price = pricingService.getPrice(order.getProductId());
            BigDecimal total = price.multiply(BigDecimal.valueOf(order.getQuantity()));
            notificationService.sendEmail(order.getId());
            return ProcessingResult.success(order.getId(), total);
        } catch (Exception e) {
            return ProcessingResult.failed(order.getId(), e.getMessage());
        }
    }
}
