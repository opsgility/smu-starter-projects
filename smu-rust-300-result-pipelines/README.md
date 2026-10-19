# Build Option/Result pipelines with combinators

Course 3 (Idiomatic Rust) Lesson 2 paired hands-on lab. You'll replace nested
`match` ladders with chained `.map` / `.and_then` / `?` pipelines, and use
`.collect::<Result<Vec<_>, _>>()` to validate a batch of inputs.

## Files

- `Cargo.toml` — package definition, no external dependencies
- `src/main.rs` — four function stubs you fill in across the exercises
- `README.md` — this file

## How to run

```bash
cargo run
```

## Per-exercise additions

| Exercise | What you add |
|---|---|
| 1 | Smoke test — observe the welcome prints + `todo!` panic |
| 2 | Implement `parse_port` with `.parse::<u16>().map_err(...)` |
| 3 | Build `load_port` as a chained `.and_then` / `?` pipeline |
| 4 | Implement `validate_all` using the `.collect::<Result<Vec<_>, _>>()` idiom |
| 5 (optional) | Add manual `.context()`-style error prefixes (preview of Lesson 3's `anyhow`) |

## Notes

- No external crates needed — pure `std`.
- Rust 2024 edition, stable 1.99.
