# smu-rust-400-closures-practice

Starter project for Course 640 (SMU-RUST-400 — Iterators, Collections, and Functional Rust), Lesson 4 paired HOL: **Fn, FnMut, FnOnce — closure drills**.

## What's here

- `Cargo.toml` — single-binary crate `closures_practice`, Rust 2024 edition, no external dependencies.
- `src/main.rs` — welcome print + five commented `// EX N:` sections. The exercises walk you through filling in one section at a time.

## How to run

```
cargo run
```

Each exercise either adds a new function and its call site, or uncomments a block in `main`. By the time you finish Exercise 5, `cargo run` prints a line for every closure drill you've built.

## Exercise additions

| Exercise | Adds | Section |
|---|---|---|
| 1 — Smoke test | Baseline `cargo run` + confirm the welcome prints. | — |
| 2 — Fn callback | `fn apply_twice<F: Fn(i32) -> i32>` + a `doubler` fn + call site. | EX 2 |
| 3 — FnMut counter | A `let mut incr = || { count += 1; count }` closure + 3 calls. | EX 3 |
| 4 — FnOnce consumer | A `move` closure that consumes a captured `String`. | EX 4 |
| 5 — Struct holding closure | `struct Handler { f: Box<dyn Fn(&str)> }` + build + call. | EX 5 |
| 6 (optional) — Return closure | `fn multiplier(k: i32) -> impl Fn(i32) -> i32` + call. | EX 6 |

## Notes

- No external dependencies. Everything is std.
- The container ships Rust 1.99 stable; `clippy` and `rustfmt` are available (`cargo clippy`, `cargo fmt`).
- Build artifacts land under `target/` and are gitignored.
