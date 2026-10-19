# smu-rust-300-dyn-shape

Starter for **Course 3 (Idiomatic Rust) Lesson 5 paired HOL** — "Heterogeneous shapes with `Vec<Box<dyn Shape>>`."

## What ships

- `Cargo.toml` — crate `dyn_shape`, edition 2024, no deps (pure std).
- `src/main.rs` — complete `trait Shape` + `Circle`/`Rectangle`/`Triangle` impls (carried forward from Lesson 4's HOL). Your job is to USE these via trait objects, not re-implement them.
- This README.

## Run

```
cargo run
```

Should print `dyn-shape starter — fill in each exercise` and nothing else — the exercises add actual output.

## Per-exercise additions

| # | What you add |
|---|---|
| 1 | Smoke test — verify starter compiles + runs. |
| 2 | Build `let shapes: Vec<Box<dyn Shape>> = vec![...]` and iterate with `describe()`. |
| 3 | Compute total area over the heterogeneous Vec via `.iter().map(.area()).sum()`. |
| 4 | Add a NOT-object-safe method (`clone_box` with `Self: Clone`) and observe the error, then apply the `where Self: Sized` fix. |
| 5 (optional) | Convert `Vec<Box<dyn Shape>>` to `Vec<&dyn Shape>` and see lifetimes come in. |

## Mentor voice

Hollis Brennan continues as the mentor across all 7 foundational courses. The LeftAgent in the lab speaks as that mentor.
