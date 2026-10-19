# smu-rust-400-iterator-basics

Starter for Course 4 Lesson 1 paired HOL — **Iterator basics — iter, iter_mut, into_iter, collect**.

## What this project is

A small Rust program with four `todo!()` function stubs that each exercise one of the three `IntoIterator` flavors (`.iter()`, `.iter_mut()`, `.into_iter()`) or the main consumption patterns (`for`, `.collect()`, terminal methods) from Lesson 1.

## How to run

```
cargo build
cargo run
```

On a fresh clone the starter prints the welcome lines and exits — none of the four functions are called from `main()` yet. Each exercise fills in one function and uncomments its matching line in `main()`.

## Per-exercise additions

| Exercise | Fills | Flavor |
|---|---|---|
| 2 | `print_each(&cities)` | `.iter()` — shared borrow, `cities` remains usable |
| 3 | `uppercase_each(&mut cities)` | `.iter_mut()` — exclusive borrow, mutate in place |
| 4 | `consume_longest(cities)` | `.into_iter()` — move, `cities` no longer usable |
| 5 | `collect_lengths(&cities)` | `.iter().map().collect()` — terminal consumption |

## Notes

- No external dependencies. Pure `std`.
- Edition 2024. Needs stable Rust 1.85+ (the `vscode-rust` container ships 1.99.1).
