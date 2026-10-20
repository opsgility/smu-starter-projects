fn main() {
    println!("ownership story — walk through five scenes.\n");

    // SCENE A — Copy primitive. Both bindings valid after assignment.
    let n: i32 = 7;
    let m = n;
    println!("SCENE A: n = {n}, m = {m}");

    // SCENE B — Move of a non-Copy value.
    let a = String::from("hello");
    let b = a;
    // TRY: println!("SCENE B after move: a = {}", a);
    println!("SCENE B: b = {b}");

    // SCENE C — Borrow. Owner stays valid, reader reads through the reference.
    let s = String::from("world");
    let r = &s;
    println!("SCENE C: s = {s}, r = {r}");

    // SCENE D — Clone. Explicit duplication; two heap allocations.
    let p = String::from("rust");
    let q = p.clone();
    println!("SCENE D: p = {p}, q = {q}");

    // SCENE E — Drop. n, m, b, s, r, p, q all go out of scope at the closing
    // brace below. Destructors for the non-Copy owners (b, s, p, q) run in
    // reverse order automatically.
    println!("\nEnd of main — every owner's destructor runs now.");
}
