package com.skillmeup.freightflow.benchmark;

import com.skillmeup.freightflow.model.Order;
import com.skillmeup.freightflow.processor.OrderProcessor;
import com.skillmeup.freightflow.processor.ProcessingResult;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;
import java.util.ArrayList;
import java.util.List;

/**
 * Runs on startup and measures order processing throughput.
 *
 * Throughput log:
 * - Baseline (sequential):           ~80 orders/sec
 * - After Lesson 2 (ThreadPoolExecutor): TODO: record result
 * - After Lesson 4 (CompletableFuture):  TODO: record result
 * - After Lesson 6 (HikariCP + batch):   TODO: record result
 * - After Lesson 8 (Caffeine cache):     TODO: record result
 */
@Component
public class BenchmarkRunner implements CommandLineRunner {
    private static final Logger log = LoggerFactory.getLogger(BenchmarkRunner.class);
    private final OrderProcessor orderProcessor;

    public BenchmarkRunner(OrderProcessor orderProcessor) {
        this.orderProcessor = orderProcessor;
    }

    @Override
    public void run(String... args) throws Exception {
        List<Order> orders = generateSampleOrders(200);

        log.info("Starting benchmark with {} orders...", orders.size());
        long start = System.nanoTime();
        List<ProcessingResult> results = orderProcessor.processAllOrders(orders);
        long elapsed = System.nanoTime() - start;

        long successCount = results.stream().filter(ProcessingResult::isSuccess).count();
        double seconds = elapsed / 1_000_000_000.0;
        double throughput = orders.size() / seconds;

        log.info("=== BENCHMARK RESULTS ===");
        log.info("Orders processed: {} / {}", successCount, orders.size());
        log.info("Time: {:.3f}s", seconds);
        log.info("Throughput: {:.1f} orders/sec", throughput);
        log.info("=========================");
    }

    public static List<Order> generateSampleOrders(int count) {
        List<Order> orders = new ArrayList<>();
        for (int i = 0; i < count; i++) {
            Order o = new Order((long)(i % 100) + 1, (i % 5) + 1);
            o.setId((long)(i + 1));
            orders.add(o);
        }
        return orders;
    }
}
