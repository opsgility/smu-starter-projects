# smu-rust-400-api-design

Starter for Course 4 (Iterators, Collections, and Functional Rust) Lesson 7 paired HOL — "Design iterator-friendly APIs".

## What's inside

- `Cargo.toml` — package `api_design`, edition 2024, no dependencies.
- `src/main.rs` — three APIs you refactor across the exercises:
  - `total(&Vec<i32>)` — restrictive, EX 2 opens it up.
  - `repeated(&str, usize) -> Vec<String>` — eager, EX 3 makes it lazy.
  - `struct Fibonacci` — fields + `new()` only, EX 4 adds the `Iterator` impl.

## How to run

```
cargo run
```

You should see:

```
total(&numbers) = 15
repeated("rust", 3) = ["rust", "rust", "rust"]
fib state: a=0, b=1
```

## Per-exercise additions

| Exercise | What you add |
|---|---|
| EX 2 | Change `total` signature to `fn total<I: IntoIterator<Item = i32>>(iter: I) -> i32`. Prove it accepts `&[i32]`, `0..10`, and a `Vec<i32>`. |
| EX 3 | Change `repeated` return type to `impl Iterator<Item = String> + '_`. Use `std::iter::repeat(s.to_string()).take(n)`. |
| EX 4 | Add `impl Iterator for Fibonacci { type Item = u64; fn next(&mut self) -> Option<u64> { ... } }`. Uncomment the `fibs` lines in `main`. |
| EX 5 (optional) | Add `fn fib() -> Fibonacci { Fibonacci::new() }`. Chain `.take(10).sum::<u64>()` from main. |
