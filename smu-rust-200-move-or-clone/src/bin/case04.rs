// case04: Try to mutate through an immutable reference.
//
// EXPECTED ERROR: E0594 — cannot assign to `*counter`, which is behind a `&`
//                 reference. (The compiler may also mention E0596 depending on
//                 the exact shape; both point at the same wrong-mutability
//                 story.)
// HINT: The `bump` function receives `counter: &i32` — a shared, read-only
//       borrow. You cannot mutate through a shared borrow.
//
// FIX ME: change the parameter type to `&mut i32` AND update the call site in
//         `main` to pass `&mut n` (and `let mut n = 0;` to make `n` itself
//         mutable). Three small changes, same intent as the broken program.

fn bump(counter: &i32) {
    *counter += 1;
}

fn main() {
    let n = 0;
    bump(&n);
    bump(&n);
    bump(&n);

    println!("n = {}", n);

    println!("case04 passed");
}
