# Lifetime annotations in practice

Starter project for the paired HOL after **Course 638 Lesson 6 — "Lifetimes made concrete"** in the Programming with Rust skill path.

Three of the four fns + the struct in `src/main.rs` are deliberately broken so the Rust compiler asks you to apply what Lesson 6 taught about lifetime annotations and the three elision rules.

## Files

| File | What's in it |
|---|---|
| `Cargo.toml` | package `lifetime_practice`, edition 2024, no deps |
| `src/main.rs` | `longest` (broken — needs `'a`), `first_word` (works via elision), `Excerpt` struct (broken — needs `'a`), `use_excerpt` (fixes itself once `Excerpt<'a>` lands) |
| `README.md` | this file |
| `.gitignore` | ignores `target/` + `Cargo.lock` |

## Run

```
cargo build
```

Initial state: three compile errors (`longest`, `Excerpt`, downstream `use_excerpt`). Walk through each exercise to apply lifetime annotations until `cargo run` prints:

```
longest = much longer than short
first word = the
excerpt = Rust lifetimes are compile-time regions, not runtime durations.
```

## Per-exercise additions

| Exercise | What you add |
|---|---|
| 1 | None — read the three compile errors with the rustc "help:" output |
| 2 | `<'a>` annotations on `longest` tying inputs to output |
| 3 | A comment on `first_word` naming the elision rule that covers it |
| 4 | `<'a>` on `Excerpt` struct; observe how `use_excerpt` ripples |
| 5 (optional) | A tiny `make_label` fn that triggers `E0597`, then its proper fix |

## Notes

- The hard constraint across the course: your student input is fenced in triple-backticks on its own line.
- Course 638 expects familiarity with Course 1's gentle ownership intro + Lesson 6's three elision rules — annotations are compile-time labels, not runtime behavior.
