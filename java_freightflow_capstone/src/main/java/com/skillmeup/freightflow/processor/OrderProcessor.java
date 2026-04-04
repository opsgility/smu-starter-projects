package com.skillmeup.freightflow.processor;

import com.skillmeup.freightflow.model.Order;
import com.skillmeup.freightflow.service.NotificationService;
import com.skillmeup.freightflow.service.ProductPricingService;
import org.springframework.stereotype.Component;
import java.math.BigDecimal;
import java.util.*;
import java.util.concurrent.*;

/**
 * Fully optimized processor: ThreadPoolExecutor + CompletableFuture + HikariCP + Caffeine + GC tuning.
 * Throughput: ~3,500 orders/sec.
 *
 * CAPSTONE — The notificationService.sendEmail() call below is still SYNCHRONOUS.
 * It blocks the processing thread for ~50ms per order.
 *
 * TODO Exercise 2: Create a dedicated notificationExecutor (Executors.newFixedThreadPool(2))
 *                  in OrderProcessorConfig (see config/OrderProcessorConfig.java)
 * TODO Exercise 3: Replace the sendEmail() call with CompletableFuture.runAsync(() -> ..., notificationExecutor)
 *                  Do NOT join() or get() — fire-and-forget
 * TODO Exercise 4: Add retry logic in NotificationService.sendEmail() — 3 retries with 100ms backoff
 * TODO Exercise 5: Add AtomicLong notificationsSent counter to NotificationService; expose via getter
 * TODO Exercise 6: Update OrderProcessorBenchmark with a new @Benchmark for async notification throughput
 * TODO Exercise 7: Fill in the final row of PerformanceReport.java — verify > 3,500 orders/sec
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
        return futures.stream().map(CompletableFuture::join).toList();
    }

    private ProcessingResult processOrder(Order order) {
        try {
            BigDecimal price = pricingService.getPrice(order.getProductId());
            BigDecimal total = price.multiply(BigDecimal.valueOf(order.getQuantity()));
            // TODO Exercise 3: Move this to a fire-and-forget CompletableFuture.runAsync()
            notificationService.sendEmail(order.getId());
            return ProcessingResult.success(order.getId(), total);
        } catch (Exception e) {
            return ProcessingResult.failed(order.getId(), e.getMessage());
        }
    }
}
