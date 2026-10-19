// drill03 — NLL (non-lexical lifetimes): a borrow ends at its last USE,
// not at the end of its lexical scope.
//
// EXPECTED: this file compiles and runs cleanly. Under the pre-NLL rules,
// this program would NOT have compiled because `r` was declared at the top of
// main and would have been considered "alive" until the closing brace. Under
// NLL (stable since Rust 2018, enabled by default in all later editions
// including 2024), the borrow ends after the last use of `r` — the println.

fn main() {
    let mut v = vec![1, 2, 3];

    // Shared borrow starts here.
    let r = &v;
    println!("shared view: {:?}", r);
    // Last use of `r` is on the line above. Under NLL, the borrow ends HERE.

    // Mutable operation on `v` is now fine — the shared borrow is already gone.
    v.push(4);
    println!("after push:  {:?}", v);

    println!("drill03 passed");
}
