# smu-rust-300-cargo-practice

Course 3 Lesson 10 hands-on practice for day-to-day Cargo workflows:
`cargo add`, feature flags, `cargo tree`, and release-profile tuning.

The starter is intentionally minimal — a one-line `main`. The lesson's five
exercises build it up step by step.

## Layout

- `Cargo.toml` — package declaration, edition 2024, starts dep-free.
- `src/main.rs` — welcome print + a comment block listing what each exercise adds.
- `.gitignore` — keeps `/target` and `Cargo.lock` out of version control.

## Run

```
cargo run
```

Expected: a single welcome line printed, no deps compiled.

## Per-exercise additions

| Exercise | What you add                                                                 |
|---------:|------------------------------------------------------------------------------|
|       1  | Verify toolchain + run the starter as-is.                                    |
|       2  | `chrono = "0.4"` + `serde = { version = "1", features = ["derive"] }` deps. |
|       3  | A `[features]` block with `default = ["pretty"]` + two `#[cfg(...)]` fns.   |
|       4  | Nothing in source — read `cargo tree` + `cargo tree -d` into `NOTES.md`.    |
|       5  | `[profile.release]` tuning for binary size.                                 |
