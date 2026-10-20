# thiserror + anyhow starter

Cargo workspace with two members:

- `config-lib/` — library crate. Owns `LoadError` (Exercise 2 derives it
  with `thiserror`) and `load_config` (Exercise 3 wires file read + line
  parse + required-key check).
- `app/` — binary crate. Exercise 4 wires `anyhow::Context` plus
  `env::args` so the student can `cargo run --package app -- ./sample.config`.

Run everything from the workspace root:

```
cargo build --workspace
cargo run --package app
cargo test --package config_lib
```
