# smu-rust-100-pattern-matching-practice

Pair-practice starter for **Lesson 7 — Pattern matching — Option, if let, destructuring** of *Programming Foundations with Rust* (SMU-RUST-100).

The lab walks you through filling in four small functions that each exercise one part of Rust's pattern-matching toolkit from Lesson 7:

| # | Function | What it practices |
|---|---|---|
| 2 | `safe_divide(a, b) -> Option<f64>` | Returning `Option`, matching on `Some`/`None` |
| 3 | `drain_and_sum(v) -> i32` | `while let Some(x) = v.pop()` loops |
| 4 | `describe_point((x, y)) -> String` | Tuple destructuring + match guards |
| 5 (optional) | `find_by_id(items, id) -> Option<&str>` | Iterator + `if let` + a first look at lifetime annotations |

## How to run

From the workspace root:

```
cargo run
```

The welcome print confirms the project compiles. Then follow the lab exercises in order — each one uncomments the next function stub, fills it in, and adds a call from `main()` so you can see it work.

## Lifetime annotation in Exercise 5

The optional Exercise 5 signature uses `fn find_by_id<'a>(items: &'a [(u32, &'a str)], id: u32) -> Option<&'a str>`. The `'a` is a **lifetime annotation**. Course 2 (The Rust Ownership Model) covers lifetimes properly. For this lab, copy the signature verbatim and read `'a` as *"the returned `&str` lives at least as long as the input slice."* Rust needs this hint because the return value borrows from the input.

## Files in this starter

- `Cargo.toml` — std-only, no external crates
- `src/main.rs` — welcome print + four commented function stubs you'll uncomment in order
- `README.md` — this file
- `.gitignore` — standard Rust target/ ignore
