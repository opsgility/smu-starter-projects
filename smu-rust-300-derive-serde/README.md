# SMU-RUST-300 Lesson 8 — Derive macros + serde in practice

Starter for the Course 3 (Idiomatic Rust) Lesson 8 paired hands-on lab. You take an `AppConfig` struct that the compiler refuses to deserialize, add the right `#[derive(...)]` and `use serde::...` lines, then round-trip the config through JSON. Along the way you add `#[serde(rename)]`, `#[serde(default)]`, and `#[serde(skip_serializing_if = "Option::is_none")]` to control how fields map to JSON.

## Scenario

Terrace Labs ships a small service that reads its config from a JSON file. The deserialization layer is Rust's `serde` + `serde_json`, both of which are already in `Cargo.toml`. You wire the struct up to those crates with derive macros, then watch the derived code do what a hand-written `impl Deserialize for AppConfig` would do with far less code.

## Files

```
smu-rust-300-derive-serde/
  README.md
  Cargo.toml           # serde + serde_json deps — already preinstalled in vscode-rust via pre-fetch
  .gitignore
  src/
    main.rs            # AppConfig struct stub + SAMPLE_JSON — exercises fill in derive attrs
```

## How to run

```
cargo run
```

Expect the smoke-test run (Exercise 1) to fail at build time because `AppConfig` doesn't derive `Deserialize` yet. Reading that compiler error is step one.

Exercise 2 adds the derives + imports and the same `cargo run` prints the parsed `AppConfig`.

## Notes

- `serde = "1"` + `serde_json = "1"` are long-stable 1.x crates. They are pre-fetched into the shared `vscode-rust` cargo registry so first `cargo build` is a warm cache.
- Edition `2024` matches the rest of the Programming with Rust skill path.
- The `api_key` value in `SAMPLE_JSON` is a visibly-fake placeholder (`sk-DEMO-NOT-REAL`) — no real secret.
