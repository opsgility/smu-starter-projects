# smu-rust-300-orphan-rule

Starter for **Course 3 Lesson 7 HOL — Work around the orphan rule — newtype and extension traits**.

## The starter is deliberately broken

`src/main.rs` opens with an `impl ToString for Vec<i32>` block that violates the orphan rule. The project does **not** compile out of the box. That is the whole point of Exercise 1 — you read the compiler error and understand why Rust refuses.

## How this evolves across the exercises

| Exercise | What you add to `src/main.rs` |
|---|---|
| 1 | Observe `cargo build` fail with E0117. Read the full error. |
| 2 | Comment the broken `impl ToString for Vec<i32>` block out. Confirm `cargo run` succeeds. Add a one-line comment stating why. |
| 3 | Define `struct IntList(Vec<i32>);` + `impl std::fmt::Display for IntList`. Print an `IntList(vec![1, 2, 3])` from `main`. |
| 4 | Define `trait Summable` with a blanket impl `impl<T: IntoIterator<Item = i32> + Clone> Summable for T`. Call `.sum_as_str()` on a `Vec<i32>` from `main`. |
| 5 (optional) | Add `impl Deref<Target = Vec<i32>> for IntList`. Call Vec methods directly on an `IntList`. |

## Run

```
cargo build
cargo run
```

Expect `cargo build` to fail with E0117 before you complete Exercise 2.

## Narrator

Hollis Brennan is your mentor across the Programming with Rust skill path.
