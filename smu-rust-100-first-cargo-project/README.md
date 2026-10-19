# Your first cargo project — SMU-RUST-100 Lesson 1 paired lab

Welcome to your first hands-on time with Rust! In Lesson 1 you watched Hollis Brennan walk through what the toolchain does — now you run the toolchain yourself.

## What you will do

Over four short exercises you will:

1. Confirm that `rustc`, `cargo`, and `rustup` are installed and reporting a current version.
2. Run `cargo new` to generate a brand new Rust project from scratch.
3. Edit the generated `src/main.rs` and `Cargo.toml`, then rebuild to see how changes flow through.
4. Build the project in release mode and compare the debug vs release binaries.

There is deliberately no code to copy or project to clone here. The whole point of this lab is that **you make the files yourself** by driving `cargo`. Everything you create during this lab lives inside the browser VS Code container at `/home/coder/workspace` and is thrown away when the lab ends.

## What's already set up for you

- Rust 1.99.x stable toolchain (via `rustup`)
- `cargo`, `rustc`, `rustfmt`, `clippy`, and the `wasm32-unknown-unknown` target
- `rust-analyzer`, `CodeLLDB`, `even-better-toml`, and `dependi` VS Code extensions
- A terminal inside VS Code to the right — press `` Ctrl+` `` if it's not already open

## How you'll know it worked

Each exercise ends with a `cargo` command whose output is quoted in the exercise text. If what you see on your terminal matches, you're ready for the next step. If it doesn't match, the left sidebar agent (Hollis Brennan) is there to help — ask a question and work through the error together.

## Vocabulary you'll meet (in order)

- `rustc` — the Rust compiler
- `cargo` — Rust's package manager + build tool
- `rustup` — the toolchain installer / version manager
- `Cargo.toml` — a Rust project's manifest (package metadata, dependencies, build config)
- `src/main.rs` — the entry point of a binary crate
- `target/debug/` — where `cargo build` puts unoptimized binaries
- `target/release/` — where `cargo build --release` puts optimized binaries

Ready? Open the first exercise in the right-hand pane.
