// ownership_story — a tiny program that walks through 5 ownership scenes.
// Across the exercises you will annotate each SCENE with what it does to
// ownership, then intentionally break SCENE B and fix it with .clone().
//
// SCENE A: value creation + a Copy type
// SCENE B: a String move
// SCENE C: a shared borrow
// SCENE D: an explicit clone
// SCENE E: scope end (drop)

fn main() {
    println!("ownership story — walk through five scenes.");
    println!();

    // SCENE A — Copy types
    let n: i32 = 7;
    let m = n;
    println!("SCENE A: n = {}, m = {}", n, m);

    // SCENE B — Non-Copy move
    let a = String::from("hello");
    let b = a;
    println!("SCENE B: b = {}", b);
    // TRY: println!("SCENE B after move: a = {}", a);

    // SCENE C — Shared borrow
    let s = String::from("world");
    let r = &s;
    println!("SCENE C: s = {}, r = {}", s, r);

    // SCENE D — Explicit clone
    let p = String::from("rust");
    let q = p.clone();
    println!("SCENE D: p = {}, q = {}", p, q);

    // SCENE E — End of main() scope: n, m, b, s, r, p, q all drop here.
    println!();
    println!("End of main — every owner's destructor runs now.");
}
