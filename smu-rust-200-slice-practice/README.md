# SMU-RUST-200 — Slice-ify practice

Pair starter for Course 638 Lesson 5 ("Slices — &[T], &str, and views into data").
Student refactors three fns from owned-container references to slices, fixes a
char-boundary panic, and implements a non-allocating tokenizer.

## Scenario

Hollis Brennan — the Course 2 mentor — hands you a small program with four
functions that each use a sub-optimal borrow shape. Course 1 taught you to
reach for `&Vec<T>` and `&String`. Course 2 teaches you the slice idioms
(`&[T]`, `&str`) that are more general and more idiomatic.

## Files

```
smu-rust-200-slice-practice/
  README.md
  .gitignore
  Cargo.toml                # slice_practice, edition 2024, std-only
  src/
    main.rs                 # 4 fns + driver — exercises refactor each one
```

## How to run

1. Open the folder in the VS Code lab container (CodeEditorType = 16, vscode-rust).
2. `cargo run` compiles and prints the current (sub-optimal but working) output.
3. Work through the four exercises in order; each one changes one or two fns
   and `cargo run` reflects the new behavior.

## Exercises land here

- **Exercise 1 — Smoke test.** `cargo run` prints the four function results
  with their current shapes.
- **Exercise 2 — Slice-ify `sum` and `count_vowels`.** Swap `&Vec<u32>` for
  `&[u32]`, `&String` for `&str`. Verify both still work AND accept more
  callers (`sum(&[1,2,3])`, `count_vowels("hi")`).
- **Exercise 3 — Fix the char-boundary panic.** Uncomment the `🦀🦀🦀` line
  and watch `first_three_chars` panic at the UTF-8 boundary. Fix it with
  `.chars().take(3).collect::<String>()` and return `String` instead of
  `&str`.
- **Exercise 4 — Implement `tokens`.** Return `Vec<&str>` of slices borrowed
  from the input. Zero per-token allocations — the slices point into the
  caller's `&str`.

## Notes

- No external dependencies. Pure std.
- No `src/bin/` — this starter is a single-binary project.
- Edition 2024 under Rust 1.99.1 stable (vscode-rust container).
- The intentional panic on `first_three_chars("🦀🦀🦀")` is the point of
  Exercise 3 — observe it, then fix it. Don't be alarmed when it happens
  during the exercise.
