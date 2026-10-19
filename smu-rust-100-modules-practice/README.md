# SMU-RUST-100 Lesson 13 — Modules practice (greeting generator)

A single-file "greeting generator" program you refactor across the lab into a proper multi-file Rust project. You exercise `mod`, `pub`, `use`, a library crate, a nested module split across files, one external dependency added via `cargo add`, and (optionally) splitting a binary out into `src/bin/`.

## Scenario

A fictional international support desk needs a tiny CLI that produces language- and time-aware greetings for its customers. The initial version ships as a single `src/main.rs`. Across the exercises you grow it into the structure a real Rust team would use for the next generation of the tool.

## Files

```
smu-rust-100-modules-practice/
  README.md
  .gitignore
  Cargo.toml                       # package = modules_practice, edition 2024, no deps
  src/
    main.rs                        # single-file greeting generator: greeting_for + format_name + build_greeting + main
```

Across the lab you will add:

| Exercise | Files added or changed |
|---------:|---|
| 1 | smoke test only — no file changes |
| 2 | `src/lib.rs` created; `greeting_for` + `format_name` moved out of `main.rs` with `pub` |
| 3 | `src/greetings.rs` created; `greeting_for` moved into it, re-exported from `lib.rs` |
| 4 | `src/clock.rs` created with `random_period()`; `rand` added to `Cargo.toml` via `cargo add rand` |
| 5 (optional) | `src/bin/greet.rs` created; `main.rs` deleted or reused |

## How to run

```
cargo run
```

Expected output after the smoke test:

```
Good morning, Camila!
```

As each exercise lands, re-run `cargo run` to confirm the program still prints the greeting (the structure changes; the behavior does not).

## Notes

- Rust toolchain in the lab container is **1.99.1 stable** on the **2024 edition** — `cargo add` is available (it was stabilized in Rust 1.62).
- Package name is `modules_practice` (underscore) in `Cargo.toml`. When you add `src/lib.rs` in exercise 2, callers reach library items via `use modules_practice::...` or the fully-qualified `modules_practice::greeting_for(...)`. The subfolder name on disk uses dashes; the Cargo package name uses underscores — this is a Rust convention and both are correct.
- The greeting data lives in `greeting_for`'s match arms. If you want to add a language, add arms for all three periods or the catchall `_ => "Hello"` arm takes over.
