# smu-rust-300-thiserror-anyhow

Starter project for the **Design error types with thiserror and anyhow** hands-on lab in **Idiomatic Rust: Traits, Generics, Error Handling** (SMU-RUST-300, Course 3 of the Programming with Rust skill path).

## What ships

A two-crate Cargo workspace that illustrates the canonical **library + application** split for Rust error handling.

```
smu-rust-300-thiserror-anyhow/
├── Cargo.toml           # [workspace] members = ["config-lib", "app"]
├── config-lib/          # Library crate — depends on `thiserror`
│   ├── Cargo.toml
│   └── src/lib.rs       # LoadError (stub) + load_config (stub)
└── app/                 # Binary crate — depends on `anyhow` + config-lib
    ├── Cargo.toml
    └── src/main.rs      # fn main() -> anyhow::Result<()> stub
```

Both stubs compile but do nothing useful — you build them out across the exercises.

## Run

Open a terminal in the lab container, then:

```
cargo build --workspace
cargo run --package app
```

`cargo run --package app` executes the welcome stub until Exercise 4 wires it up for real.

## Per-exercise additions

| # | What you add |
|---|---|
| 1 | Nothing — just confirm the workspace builds and the welcome prints. |
| 2 | Design `LoadError` enum in `config-lib/src/lib.rs` with `thiserror::Error` + three variants (`IoError`, `ParseError`, `MissingKey`). Add a unit test. |
| 3 | Implement `load_config` for real — read the file, parse `key=value` lines, validate required keys, propagate errors with `?`. |
| 4 | Wire `app/src/main.rs` to accept a path from `std::env::args`, call into `config_lib`, use `.context()` to add a frame. |
| 5 | (Optional) Trigger each failure mode and compare the formatted error chains. |

## Why the split?

Libraries want precise, enum-shaped error types callers can match on. Applications want to just propagate anything — `anyhow::Error` is a type-erased wrapper that holds any `std::error::Error` + an error chain. The pattern this lab practices is **library returns thiserror enum; application wraps with anyhow**, which is the de-facto community standard in 2026.
