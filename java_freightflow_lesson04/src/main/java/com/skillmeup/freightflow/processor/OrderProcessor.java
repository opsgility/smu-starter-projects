package com.skillmeup.freightflow.processor;

import com.skillmeup.freightflow.model.Order;
import com.skillmeup.freightflow.service.NotificationService;
import com.skillmeup.freightflow.service.ProductPricingService;
import org.springframework.stereotype.Component;
import java.math.BigDecimal;
import java.util.*;
import java.util.concurrent.*;

/**
 * Processes orders using ThreadPoolExecutor.
 * Baseline throughput with this implementation: ~520 orders/sec.
 *
 * TODO Exercise 2: Convert each Callable submission to CompletableFuture.supplyAsync(() -> ..., executor)
 * TODO Exercise 3: Chain .thenApply(result -> enrichResult(result)) to add a processing timestamp
 * TODO Exercise 4: Add .exceptionally(ex -> ProcessingResult.failed(orderId, ex.getMessage()))
 * TODO Exercise 5: Combine all futures with CompletableFuture.allOf(...).join()
 * TODO Exercise 6: Run BenchmarkRunner — record throughput above
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
        List<Future<ProcessingResult>> futures = new ArrayList<>();

        for (Order order : orders) {
            Callable<ProcessingResult> task = () -> processOrder(order);
            futures.add(executor.submit(task));
        }

        List<ProcessingResult> results = new ArrayList<>();
        for (Future<ProcessingResult> future : futures) {
            try {
                results.add(future.get(10, TimeUnit.SECONDS));
            } catch (Exception e) {
                results.add(ProcessingResult.failed(-1L, e.getMessage()));
            }
        }

        // TODO Exercise 2-5: Replace Future.get() loop with CompletableFuture pipelines

        return results;
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
