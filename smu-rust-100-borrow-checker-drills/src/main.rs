// This project ships 12 broken drill programs under src/bin/drill01.rs through
// src/bin/drill12.rs. Run each one with `cargo run --bin drillNN`, read the
// compiler error, apply the smallest fix, re-run until it prints
// `drill NN passed`.
//
// You don't need to run this main.rs — it's here so `cargo build` keeps a
// sensible default binary. Jump straight to `cargo run --bin drill01`.

fn main() {
    println!("borrow-checker drills — start with `cargo run --bin drill01`");
    println!("see README.md for the full exercise walkthrough");
}
