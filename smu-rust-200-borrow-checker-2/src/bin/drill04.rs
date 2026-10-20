// EXPECTED ERROR: E0499 — cannot borrow `v` as mutable more than once at a time
// HINT: Both `a` and `b` are `&mut v` and alive simultaneously. NLL reorder:
//       use `a` to completion, THEN create `b`. Each mutable borrow lives
//       from its creation to its last use.
// FIX ME: Make this compile.

fn main() {
    let mut v = vec![1, 2, 3];

    let a = &mut v;
    let b = &mut v;

    a.push(10);
    b.push(20);

    println!("v = {v:?}");
}
