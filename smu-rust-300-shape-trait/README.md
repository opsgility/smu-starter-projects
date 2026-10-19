# shape-trait

Starter for the SMU-RUST-300 (Idiomatic Rust) Lesson 4 paired hands-on lab —
**Design a Shape trait with default methods**.

Three structs are defined for you: `Circle`, `Rectangle`, `Triangle`. Across
the exercises you build:

1. (Ex 1) Smoke test — run `cargo run` and read the welcome.
2. (Ex 2) Define `trait Shape { fn area(&self) -> f64; fn perimeter(&self) -> f64; fn describe(&self) -> String { ... } }` with a default `describe` that uses the two required methods.
3. (Ex 3) Implement `Shape` for all three types. Override `describe` for `Rectangle` to add a shape-specific label.
4. (Ex 4) Write `fn report<S: Shape + std::fmt::Debug>(s: &S) { ... }` and call it with each shape.
5. (Ex 5, optional) Write `fn total_area<S: Shape>(shapes: &[S]) -> f64` and call with a `Vec<Circle>`. Observe that mixing types in the same `Vec` needs `dyn Trait` (Lesson 5).

## Run

```bash
cargo run
```

## Files

- `Cargo.toml` — package metadata, no external deps.
- `src/main.rs` — three structs defined, trait + impls + fns to be written.
