# SMU-RUST-300 Lesson 9 — Workspace split

A deliberately-small single-crate Rust program that you refactor across five
exercises into a cargo workspace with a reusable `shapes-core` library and a
`shapes-cli` binary. Practices `mod`, `pub`, `use`, `path =` deps between
member crates, and `[workspace.dependencies]` sharing.

## Scenario

Hollis Brennan at Terrace Labs needs the shape-rendering code reused across
two internal tools — a reporting CLI (`shapes-cli`) and an upcoming web
dashboard. Today the whole thing lives in `main.rs`. By the end of the lab
the shape logic has been split out of `main.rs` into its own file (Exercise
2), then promoted to a sibling library crate inside a cargo workspace
(Exercise 3), with a shared workspace-level dependency (Exercise 4) and an
integration test on the trait (optional Exercise 5).

## Files

```
smu-rust-300-workspace-split/
  README.md                        # this file
  Cargo.toml                       # single-crate; becomes the workspace root in Ex 3
  src/
    main.rs                        # ~60 lines — Shape trait + Circle + Rectangle + print_shapes + main
  .gitignore
```

By the end of the lab the project looks like:

```
smu-rust-300-workspace-split/
  Cargo.toml                       # [workspace] members = ["shapes-core", "shapes-cli"]
  shapes-core/
    Cargo.toml
    src/lib.rs
  shapes-cli/
    Cargo.toml                     # path = "../shapes-core" dep
    src/main.rs
```

## How to run

```
cargo run
```

Prints the two shape descriptions. After Exercise 3 (workspace), run
specific crates with `cargo run -p shapes-cli` and run per-crate tests with
`cargo test -p shapes-core`.

## Notes

- `rand` dependency added in Exercise 4 is already preinstalled in the
  `vscode-rust` container variant's cargo registry; `cargo add rand` writes
  to `Cargo.toml` without a network fetch.
- No `.env` and no cloud backing — pure local Rust refactoring.
