// drill03 — NLL (non-lexical lifetimes).
//
// Compiles as shipped. The shared borrow `r` ends at its last use (the
// println), not at the closing brace of the enclosing block — so the
// subsequent `v.push(4)` is legal.

fn main() {
    let mut v = vec![1, 2, 3];

    let r = &v;
    println!("shared view: {:?}", r);

    v.push(4);
    println!("after push:  {:?}", v);
    println!("drill03 passed");
}
