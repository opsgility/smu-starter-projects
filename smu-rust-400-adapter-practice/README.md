# smu-rust-400-adapter-practice

Starter for Course **SMU-RUST-400** (Iterators, Collections, and Functional Rust) — Lesson 2 paired hands-on lab.

You take five functions that each do their work with a plain `for` loop and refactor each one into the equivalent iterator-adapter chain. The behavior stays the same; only the shape changes.

## Files

- `Cargo.toml` — edition 2024, no dependencies (pure std).
- `src/main.rs` — five functions each with a WORKING imperative body and a `// TODO: refactor to adapter chain` comment. Main drives them and prints the output.

## Run

```bash
cargo run
```

Expected output on the shipped starter:

```
adapter-practice starter — see README.md

sum_evens: 30
double_strings: ["alpha-alpha", "beta-beta", "gamma-gamma"]
zip_names_ages: ["Imani is 42", "Pavel is 37", "Kenji is 29"]
flatten_sublists: [1, 2, 3, 4, 5, 6]
count_matching(> 5): 5
```

## What each exercise adds

| Exercise | What you refactor |
|---------:|-------------------|
| 1 | Smoke test — all five functions compile and produce the expected output under their imperative bodies. |
| 2 | `sum_evens` → `.iter().filter(...).sum()`. |
| 3 | `double_strings` + `zip_names_ages` → `.iter().map(...).collect()` and `.iter().zip(...).map(...).collect()`. |
| 4 | `flatten_sublists` + `count_matching` → `.into_iter().flatten().collect()` and `.iter().filter(...).count()`. |
| 5 | (Optional) Write a new `fold_product` using `.iter().fold(1, |acc, &x| acc * x)` and compare with the equivalent `for` loop. |

## Notes

The output lines never change across the refactor. If `cargo run`'s output drifts, the refactor is wrong — compare the adapter chain against the imperative body and check your closures.
