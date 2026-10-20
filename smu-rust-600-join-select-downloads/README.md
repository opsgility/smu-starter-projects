# smu-rust-600-join-select-downloads

Starter for Course 6 Lesson 6 — Concurrent downloads with join! and select!.

Mocked fetchers live in `src/lib.rs` so no network dependency.

```
cargo run --bin sequential
cargo run --bin concurrent
cargo run --bin race
cargo run --bin try_join
```
