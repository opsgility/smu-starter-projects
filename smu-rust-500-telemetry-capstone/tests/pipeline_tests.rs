// Integration tests for the capstone pipeline.
//
// These tests exercise the shape the student builds across Exercises 2-4.
// Exercise 2 (ingest + bounded channel + registry) makes test_ingest_throughput pass.
// Exercise 3 (Rayon aggregation + atomic counters) makes test_registry_concurrency pass.
// Exercise 4 (graceful shutdown) makes test_graceful_shutdown pass.
//
// Starter versions of these tests are stubbed; the student fills in `fn run_pipeline`
// in src/main.rs (or a shared lib) as they go.

#[test]
fn test_ingest_throughput() {
    // Starter stub — passes trivially until Exercise 2 lands.
    // Exercise 2 asserts: `run_pipeline(duration=2s).packets_in >= 1000`.
    assert!(true, "fill in via Exercise 2 of Lab 3331");
}

#[test]
fn test_registry_concurrency() {
    // Starter stub — Exercise 3 fills this in.
    assert!(true, "fill in via Exercise 3 of Lab 3331");
}

#[test]
fn test_graceful_shutdown() {
    // Starter stub — Exercise 4 fills this in.
    assert!(true, "fill in via Exercise 4 of Lab 3331");
}
