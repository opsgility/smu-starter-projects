# Fix the borrow checker 2.0 — 12 harder drills

Twelve small programs that each fail to compile because of a specific borrow-checker error. Your job: read the compiler message, locate the problem, apply the smallest fix that makes the program compile AND print its expected success line.

These are HARDER than the Course 1 "Fix the borrow checker" drills (Lab 3262). Each drill is 15–20 lines and the fix is not always at the obvious place.

## How to run each drill

```
cargo run --bin drill01
cargo run --bin drill02
...
cargo run --bin drill12
```

Each drill ships broken. The compiler message tells you exactly what's wrong — your job is to read it carefully and apply the right fix.

## Expected success line

Each fixed drill should print a human-readable line showing its intended output (e.g. `sum 1..=5 = 15`, `v = [1, 10, 2, 3]`, `first was: alpha`). The line is in the drill's `println!` call — if the fix is correct, the program compiles and prints that line.

## Drill index

| Drill | Error  | Family                                           |
|:-----:|:-------|:-------------------------------------------------|
| 01    | E0382  | use after move inside a loop                     |
| 02    | E0505  | move while shared borrow outstanding             |
| 03    | E0502  | mut while shared, through same struct field      |
| 04    | E0499  | two mut borrows (NLL re-order fix)               |
| 05    | E0596  | method takes `&self` but needs `&mut self`       |
| 06    | E0384  | immutable binding (fix at the right line)        |
| 07    | E0507  | move out of Vec index                            |
| 08    | E0515  | returning `&str` from local `String`             |
| 09    | E0507  | move out of struct field through `&`             |
| 10    | E0382  | move via `into_iter()` desugar in `for` loop     |
| 11    | E0499  | two mut borrows in a single expression           |
| 12    | E0597  | struct holds `&str`, outlives the String         |

## Troubleshooting

- If the compiler error says `cannot find crate` or `could not find Cargo.toml`, check you're in the lab's workspace root: `cd ~/workspace`.
- If `cargo run --bin drillNN` says `main function not found`, confirm `src/bin/drillNN.rs` exists and has a `fn main() {}`.
- If a drill compiles on the FIRST try, something is wrong — the shipped state is intentionally broken. Re-check you have the latest starter.

## Narrator

Hollis Brennan — your Rust mentor across the Programming with Rust path. Hollis Brennan will prompt you when you get stuck. Read the compiler message first, then ask for a hint if you need one.
