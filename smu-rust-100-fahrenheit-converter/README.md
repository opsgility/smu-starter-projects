# SMU-RUST-100 Lesson 5 — Fahrenheit/Celsius Converter CLI

Starter scaffold for Lesson 5 of **Programming Foundations with Rust** (course 637). You start with an empty `main()` and a stub Cargo manifest; the lab exercises walk you through growing it into a small working CLI that converts between Fahrenheit and Celsius.

## Scenario

Hollis Brennan, your Rust mentor, has given you a classic first-program exercise. By the end of the lab you will have a program you can run from the terminal: pass it a direction (`f_to_c` or `c_to_f`) and a number, and it prints the converted temperature. The lesson exercises every concept covered in Lessons 1–4: `cargo new` + `cargo run`, variables + `let mut`, functions with typed signatures, `match`, and basic error handling with `.expect()`.

## Files

```
smu-rust-100-fahrenheit-converter/
  README.md                 # This file.
  .gitignore                # Ignores target/, Cargo.lock, editor junk, .env.
  Cargo.toml                # Package manifest. Package name: fahrenheit_converter, edition 2024, no deps beyond std.
  src/
    main.rs                 # Stub main() with TODOs marking what each exercise step adds.
```

## How to run

The `vscode-rust` lab container already ships Rust 1.99.1 stable + Cargo. You do **not** install anything — just build and run.

1. In the integrated terminal:

```
cargo build
```

   The first build takes 10–20 seconds while Cargo compiles the empty project. Subsequent builds are near-instant.

2. Run the starter as-is to confirm the environment works:

```
cargo run
```

   You should see the two welcome lines from `main()`. If you do, you're ready to start Exercise 2.

## What each exercise adds

| Exercise | What you add |
|---|---|
| 1 | Open the project, run `cargo build` + `cargo run` once as a smoke test. |
| 2 | `fn fahrenheit_to_celsius(f: f64) -> f64` + a hard-coded call from `main()`. |
| 3 | The reverse `fn celsius_to_fahrenheit(c: f64) -> f64` + a `match` on a direction string. |
| 4 | Read the direction and value from `std::env::args()` instead of hard-coding them. |
| 5 (optional) | Loop with `std::io::stdin().read_line()` to make a mini-REPL that exits on `quit`. |

Each exercise builds on the previous one — do them in order.

## Notes

- Edition 2024 — all code examples in the lesson materials assume `edition = "2024"` in `Cargo.toml`. The starter is already pinned there.
- No external crates. Everything the exercises need lives in `std`.
- `target/` and `Cargo.lock` are gitignored. The lab container's workspace is ephemeral, so there's no cross-session persistence to worry about.
- If a build fails with a cryptic error, re-read the exercise's expected diff — the single most common Beginner trip here is forgetting that `cargo run` picks up `src/main.rs` only (not scratch `.rs` files you created elsewhere).
