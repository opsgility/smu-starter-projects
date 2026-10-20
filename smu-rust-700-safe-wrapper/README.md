# smu-rust-700-safe-wrapper

Starter for Course 7 Lesson 2 — wrap `std::slice::from_raw_parts` in a safe public API.

```
cargo build
cargo run
cargo test
```

Exercises:
1. Smoke test — verify toolchain + starter files.
2. Replace `view`'s `todo!()` with a safe wrapper around `from_raw_parts`.
3. Explain and remove the unsound `bad_view` function.
