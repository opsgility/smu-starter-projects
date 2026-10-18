# Guess the Number — Starter

Starter project for the SkillMeUp lab **Build a guess-the-number game** (course `SMU-RUST-100`, Lesson 9).

## What you build

A classic console game: the program picks a secret number between 1 and 100, you guess, it tells you "too low", "too high", or "correct!" — and it counts how many tries it took.

Across the lab's five exercises you'll grow this empty `main()` into a working game, exercising everything from Lessons 1–8:

- Variables + mutability
- Functions
- `loop` + `match`
- `std::io::stdin()` for reading input
- `.parse()` returning `Result`
- The `?` operator and `Result`-based error handling
- Adding external crates with `cargo add` (first time!)

## How to run

```
cargo run
```

The starter prints a welcome line. Each exercise adds the next piece.

## Files

- `Cargo.toml` — package manifest. `rand` is deliberately absent; Exercise 2 teaches you `cargo add rand`.
- `src/main.rs` — your game lives here. Edit it as you progress through the lab.
