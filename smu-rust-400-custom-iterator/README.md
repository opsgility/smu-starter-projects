# smu-rust-400-custom-iterator

Starter for **Course 640 Lesson 3 paired HOL — "Implement your own iterators"**
(Programming with Rust skill path).

## What this project is

Two custom iterators to implement:

1. **`Fibonacci`** — yields `u64` values forever. Demonstrates the "named
   state" pattern: a struct holds `a` and `b` fields, `next` advances them.
2. **`Words<'a>`** — yields `&'a str` slices (non-empty, whitespace-separated)
   from a borrowed source string. Demonstrates lifetimes in iterator state.

The starter ships both struct declarations but **no `Iterator` impl**. Each
exercise adds one implementation.

## Files

| Path | Role |
|---|---|
| `Cargo.toml` | Pure `std` crate; no deps. |
| `src/main.rs` | The two struct declarations + a stub `main` with four commented call sites. |
| `README.md` | This file. |

## Running

```
cargo run
```

Prints the welcome lines. As you work through each exercise, uncomment the
matching block in `main` to see the new iterator at work.

## Per-exercise additions

| # | What you add | File |
|---:|---|---|
| 1 | Smoke test — just `cargo run` + `cargo build`. | — |
| 2 | `impl Iterator for Fibonacci` | `src/main.rs` |
| 3 | `impl Iterator for Words<'a>` | `src/main.rs` |
| 4 | `size_hint` on Fibonacci + `count` override on Words | `src/main.rs` |
| 5 | (Optional) `fn fibonacci_closure()` using `std::iter::from_fn` | `src/main.rs` |
