# smu-rust-500-shared-registry

Starter for Lab 3324 (Course 5, Lesson 8) — Shared registry with Arc, Mutex, RwLock.

Single-threaded `HashMap<String, Station>` baseline. The exercises walk the student through wrapping in `Arc<Mutex<_>>`, then swapping to `Arc<RwLock<_>>` and measuring the read-heavy win.

Course 5 — Concurrent Rust (SMU-RUST-500).
