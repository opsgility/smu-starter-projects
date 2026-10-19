# SMU-RUST-100 — Design a shopping cart with structs

Starter project for the Lesson 11 paired hands-on lab in Programming Foundations with Rust (course `smu-rust-100`). You build a small shopping-cart domain model that exercises Lesson 11 concepts: `struct`, `impl`, derived traits (`Debug`, `Clone`), associated functions vs methods, and the operational distinction between `&self`, `&mut self`, and `self` receivers.

## Scenario

You are building a tiny shopping cart library for a learning exercise. A cart holds a list of items; each item has a name, a per-unit price in cents, and a quantity. You add items to the cart, compute totals, print a human-readable receipt, and in the optional final exercise you watch the compiler tell you a cart that was `consume`d is gone forever.

## Files

```
smu-rust-100-shopping-cart/
  README.md
  Cargo.toml                 # package: shopping_cart, edition 2024, no deps
  .gitignore                 # /target, Cargo.lock, editor noise
  src/
    main.rs                  # welcome print + 4 commented stubs for Ex 2-5
```

## How to run

```
cargo run
```

The starter prints the welcome line. Each exercise fills in one of the commented stubs; `cargo run` after each exercise shows the output described in the exercise text.

## Per-exercise additions

| Exercise | Adds |
|---|---|
| 1 | Smoke test — nothing new; verify the starter compiles and prints the welcome line. |
| 2 | `struct CartItem` with `#[derive(Debug, Clone)]`; `CartItem::new(...)` + `.subtotal_cents(&self)`. |
| 3 | `struct Cart` with `#[derive(Debug, Clone)]`; `Cart::new()` + `Cart::add(&mut self, item: CartItem)`. |
| 4 | `Cart::total_cents(&self) -> u32` and `Cart::describe(&self) -> String`. |
| 5 (optional) | `struct Receipt` + `Cart::consume(self) -> Receipt` — demonstrates by-value `self` and the `E0382 use of moved value` compile error. |

## Notes

- Prices are stored as `u32` cents, not `f64` dollars — floating-point money is a classic bug source, and cents-as-ints is the normal real-world fix. The exercises format cents as dollars at display time only.
- No external crates. Pure `std`.
- The commented stubs in `src/main.rs` are **comments on purpose** — if you uncomment them before you have the struct definitions above, the file will not compile. Fill them in exercise order; each exercise's final-state code is shown in the exercise text.
