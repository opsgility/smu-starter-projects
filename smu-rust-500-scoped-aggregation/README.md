# smu-rust-500-scoped-aggregation

Starter for Lab 3326 (Course 5, Lesson 10) — Scoped parallel aggregation.

1 M-record generator + serial baseline. The exercises use `std::thread::scope` to parallelize the aggregation with borrowed slices (no Arc), then add on-stack `AtomicBool` for fail-fast.

Course 5 — Concurrent Rust (SMU-RUST-500).
