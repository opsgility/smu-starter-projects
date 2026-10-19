# smu-rust-300-capstone-mini-grep

Course 3 (Idiomatic Rust: Traits, Generics, Error Handling) capstone — build a mini-grep CLI that synthesizes everything you learned across the course.

## What you ship by the end

- A `grep-core` library crate with a `Pattern` trait (Literal + Regex impls), a `Source` trait (File + Stdin impls), and a thiserror-based `GrepError` enum.
- A `grep-cli` binary crate that parses args with clap, picks the right pattern/source at runtime, and runs with `anyhow::Context`-wrapped errors.
- A cargo workspace with shared `[workspace.dependencies]`.

By the end you can run:

```
cargo run -p grep-cli -- "nation" fixtures/sample.txt
cargo run -p grep-cli -- --regex "n[aei]tion" fixtures/sample.txt
cat fixtures/sample.txt | cargo run -p grep-cli -- --regex "liberty"
```

## File layout (starter)

```
smu-rust-300-capstone-mini-grep/
├── Cargo.toml                          ← workspace root with [workspace.dependencies]
├── fixtures/
│   └── sample.txt                      ← Gettysburg Address (public domain) — grep target
├── grep-core/
│   ├── Cargo.toml                      ← thiserror + regex (via workspace)
│   └── src/
│       ├── lib.rs                      ← declares the three sub-modules
│       ├── error.rs                    ← empty, Exercise 2 fills in GrepError
│       ├── pattern.rs                  ← empty, Exercise 3 fills in Pattern + Literal + Regex
│       └── source.rs                   ← empty, Exercise 4 fills in Source + FileSource + StdinSource
└── grep-cli/
    ├── Cargo.toml                      ← anyhow + clap + serde + path dep on grep-core
    └── src/
        └── main.rs                     ← welcome stub, Exercise 5 wires everything together
```

## Per-exercise additions

| Exercise | What you add |
|---|---|
| 1 | Smoke test — `cargo build --workspace`, `cargo run -p grep-cli` prints welcome, every stub module compiles empty. |
| 2 | `grep-core/src/error.rs` — `GrepError` enum with `#[derive(thiserror::Error, Debug)]`, three variants (Io, InvalidPattern, SourceClosed). Unit tests for construction + Display. |
| 3 | `grep-core/src/pattern.rs` — `Pattern` trait, `Literal(String)` + `Regex(regex::Regex)` structs with `impl Pattern`. `Regex::try_new` returns `Result<Self, GrepError>`. |
| 4 | `grep-core/src/source.rs` — `Source` trait returning a line iterator, `FileSource` + `StdinSource` impls. Error type is `GrepError`. |
| 5 | `grep-cli/src/main.rs` — clap `Args` with `pattern`, optional `path`, `--regex` flag. `fn run<P: Pattern>(p: P, s: Box<dyn Source>) -> anyhow::Result<()>` wires everything. Uses `.context("...")` on IO. |
| 6 (optional) | Optional config file at `./minigrep.json` loaded via serde with `#[serde(default)]`. Round-trips end-to-end. |

## How to run

```
cargo build --workspace
cargo run -p grep-cli
cargo run -p grep-cli -- "nation" fixtures/sample.txt
cargo test --workspace
```

The LeftAgent pane follows along per exercise — ask for a Hint before a Full answer, and the pane keeps your mentor voice (Hollis Brennan) consistent with the rest of the course.
