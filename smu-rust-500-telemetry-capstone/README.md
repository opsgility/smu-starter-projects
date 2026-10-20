# smu-rust-500-telemetry-capstone

Starter for Lab 3331 (Course 5, Lesson 15, CAPSTONE) — Real-time telemetry pipeline.

Full-pipeline capstone. Starter provides:
- `types.rs` — `RawPacket`, `Reading`, `Station`, `WindowStats` + `parse` + merge helpers.
- `feed.rs` — a `MockFeed` that emits packets at a configurable rate.
- `main.rs` — stub `main` with every pipeline stage marked `todo!()`.
- `tests/pipeline_tests.rs` — three integration tests that light up as the student completes each exercise.

The student wires: threads for ingest, bounded channel for backpressure, `Arc<RwLock<HashMap>>` for the shared station registry, Rayon for per-window aggregation, atomic counters for observability, and `Arc<AtomicBool>` for graceful shutdown.

Course 5 — Concurrent Rust (SMU-RUST-500).
