# Enum + match in practice — exhaustive, guards, let-else

Course 639 (Idiomatic Rust: Traits, Generics, Error Handling) — Lesson 1
paired hands-on lab.

## Scenario

You are implementing a tiny request-routing function for Northhollow Analytics'
internal metrics service. Requests arrive as an `enum Request`; your `handle`
function needs to route each variant to the right output.

Everything in this lab exercises Course 639 Lesson 1:

- Exhaustive `match` on an enum (the compiler forces coverage).
- Match guards (`if payload.is_empty()`).
- Nested destructuring (`Submit { id, payload }`).
- `let-else` for the "unwrap or early-return" idiom.
- `@` binding to name a sub-range.

## Files

| Path | Purpose |
|---|---|
| `src/main.rs` | `enum Request` + a stub `handle` + `main` with sample requests |
| `Cargo.toml` | Package metadata, no external deps |
| `README.md` | This file |

## Running

```
cargo run
```

Before Exercise 3 lands, `cargo run` will panic in `handle` with the `todo!()`
message. That is expected — Exercise 3 is where you make it work.

## Per-exercise additions

| Exercise | What you add |
|---|---|
| 1 | Smoke test — just `cargo run` and read the welcome. |
| 2 | Add the missing `Metrics { verbose: bool }` variant to the enum. |
| 3 | Replace `todo!()` with an exhaustive `match` + a guard on empty-payload Submit. |
| 4 | Add a `let-else` to short-circuit on non-Submit variants. |
| 5 (optional) | Add an `@` binding to recognise `Submit { id: n @ 1..=100, .. }`. |

Zero external crates. Pure standard-library Rust 2024, Rust 1.99.
