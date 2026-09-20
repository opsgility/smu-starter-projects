package com.skillmeup.freightflow.benchmark;

/**
 * GC Tuning Comparison Report — Lesson 12
 * Fill in each row after running benchmarks with different GC flags.
 *
 * Run command example:
 *   java -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -Xms512m -Xmx2g -jar target/freightflow.jar
 *
 * | GC Configuration                        | Throughput (ops/sec) | Avg GC Pause (ms) | Max GC Pause (ms) |
 * |-----------------------------------------|----------------------|-------------------|-------------------|
 * | Default (G1GC, no flags)                |       TODO           |      TODO         |      TODO         |
 * | G1GC + MaxGCPauseMillis=200             |       TODO           |      TODO         |      TODO         |
 * | G1GC + sized heap (512m-2g)             |       TODO           |      TODO         |      TODO         |
 * | ZGC (-XX:+UseZGC)                       |       TODO           |      TODO         |      TODO         |
 * | Best configuration (your choice)        |       TODO           |      TODO         |      TODO         |
 *
 * TODO Exercise 5: Record the configuration that achieves best throughput and apply it
 * to application.properties as JVM args.
 */
public class GcTuningReport {
    // No code needed — fill in the table above
}
