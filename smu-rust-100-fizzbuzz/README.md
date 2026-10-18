# FizzBuzz and more — SMU-RUST-100

Hands-on practice for Lesson 3 of **Programming Foundations with Rust**: control flow (`if`, `else`, `loop`, `while`, `for`, `match`). The starter ships a program that compiles and prints a welcome line. Each exercise adds one function.

## Running the project

In the VS Code terminal:

```
cargo run
```

You should see `fizzbuzz starter — build out each exercise` on first run.

As you work through the exercises, call each new function from `main()` so `cargo run` shows the output you built.

## What each exercise adds

| Exercise | Function | What it exercises |
|---:|---|---|
| 1 | — | Smoke-test the toolchain. |
| 2 | `fizzbuzz_if_else(n)` | `for` over an inclusive range + `if` / `else if` / `else`. |
| 3 | `fizzbuzz_match(n)` | `match` on a tuple pattern. |
| 4 | `count_down_from(start)` | `loop` + mutable binding + `break`. |
| 5 | `sum_1_to_n(n) -> u32` | `for` with an accumulator + returning a value. |

## Files

- `Cargo.toml` — Rust 2024 edition, no external dependencies. Everything you need is in the standard library.
- `src/main.rs` — the welcome print plus four commented-out function stubs. Uncomment each as you reach the matching exercise.

## Troubleshooting

- **`error: could not find Cargo.toml`** — your terminal is not in the project directory. Run `cd /home/coder/workspace` first.
- **`non-exhaustive patterns`** on a `match` — add the `_` catchall arm, or (for tuple matches) make sure every combination has a pattern.
- **Missing semicolon on the last line of a function body** is fine — that's the implicit return. **Adding** a semicolon converts the value into `()` and is one of the most common Beginner trips in Rust.
