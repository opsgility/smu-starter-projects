# SMU-RUST-100 Lesson 10 — Build a word-frequency counter

A small command-line program that reads a text file and reports its most frequent words. You will grow an empty `main` into a working CLI that reads a fixture file, tokenizes it, counts the words with a `HashMap<String, u32>`, sorts the result, and prints the top-N.

## Scenario

You are learning Rust at Terrace Labs, a small software consultancy. Hollis Brennan — your Rust mentor across this course — has handed you a text file and asked for a tool that answers "what are the most common words in this text?" By the end of the lab you have a tool you can point at any text file and get an answer in a few milliseconds — the shape of problem Rust solves well.

## Files

```
smu-rust-100-word-frequency/
  README.md
  .gitignore                    # Ignores target/ build output.
  Cargo.toml                    # Edition 2024, no dependencies — pure std.
  src/
    main.rs                     # Welcome-print stub — exercises fill it in.
  fixtures/
    sample.txt                  # Lincoln's Gettysburg Address (~272 words, public domain).
                                # Attribution header is a `//` comment, deliberately counted
                                # as a word by the tokenizer — lesson 3 shows how to filter it.
```

## How to run

The container has Rust 1.99.1 stable + Cargo pre-installed; no additional setup required.

1. Open a terminal in VS Code (Terminal → New Terminal, or `` Ctrl+` ``).
2. Confirm the toolchain:
   ```
   cargo --version
   ```
3. Build and run the starter:
   ```
   cargo run
   ```
   You should see `word-frequency starter — see README.md`.

Each exercise builds on the previous one — complete them in order.

## Notes

- `fixtures/sample.txt` is Abraham Lincoln's Gettysburg Address, included for its length (short enough to inspect visually, long enough for frequency counts to mean something) and its public-domain status. The first line is a `//`-prefixed attribution comment that the tokenizer initially counts as text — lesson 3 exercises the student's filter logic to drop or keep it.
- The project ships with no third-party dependencies by design — the entire lab uses the Rust standard library (`std::fs`, `std::collections::HashMap`, `std::env`). First dependency management lives in a different lab.
- `Cargo.toml` targets `edition = "2024"` — the current Rust edition on stable Rust 1.99.
