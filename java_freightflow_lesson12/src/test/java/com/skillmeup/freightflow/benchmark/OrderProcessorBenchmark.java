package com.skillmeup.freightflow.benchmark;

import com.skillmeup.freightflow.model.Order;
import com.skillmeup.freightflow.processor.OrderProcessor;
import com.skillmeup.freightflow.processor.ProcessingResult;
import com.skillmeup.freightflow.service.NotificationService;
import com.skillmeup.freightflow.service.ProductPricingService;
import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.infra.Blackhole;
import java.util.List;
import java.util.concurrent.TimeUnit;

/**
 * JMH Benchmark for the FreightFlow Order Processor.
 *
 * This class is pre-configured with the completed benchmark methods from Lesson 10.
 * Lesson 12 exercises use these benchmarks to measure the impact of GC tuning.
 *
 * TODO Exercise 5 (Lesson 12): Add a main() method to run with -prof gc
 * TODO Exercise 5 (Lesson 12): Record gc.alloc.rate in PerformanceReport comments
 */
@BenchmarkMode(Mode.Throughput)
@OutputTimeUnit(TimeUnit.SECONDS)
@State(Scope.Benchmark)
@Fork(value = 1)
@Warmup(iterations = 2, time = 1)
@Measurement(iterations = 3, time = 2)
public class OrderProcessorBenchmark {

    private OrderProcessor orderProcessor;
    private ProductPricingService pricingService;
    private List<Order> sampleOrders;

    @Setup(Level.Trial)
    public void setup() {
        pricingService = new ProductPricingService();
        NotificationService notificationService = new NotificationService();
        orderProcessor = new OrderProcessor(pricingService, notificationService);
        sampleOrders = BenchmarkRunner.generateSampleOrders(100);
    }

    @Benchmark
    public List<ProcessingResult> measureBatchProcessing() {
        // TODO Lesson 12: Run with -prof gc and record gc.alloc.rate in PerformanceReport
        return orderProcessor.processAllOrders(sampleOrders);
    }

    @Benchmark
    public void measurePriceLookup(Blackhole bh) {
        bh.consume(pricingService.getPrice(42L));
    }
}
