// EXPECTED ERROR: E0594 — cannot assign to `*counter` which is behind a `&` reference
// HINT: `bump(counter: &i32)` takes a shared reference, which does not
//       permit mutation. Three edits land the fix: parameter type -> `&mut
//       i32`, binding -> `let mut n = 0;`, call sites -> `bump(&mut n);`.
// FIX ME: Make this program compile and print `case04 passed`.

fn bump(counter: &i32) {
    *counter += 1;
}

fn main() {
    let n = 0;
    bump(&n);
    bump(&n);
    bump(&n);
    println!("n = {n}");
    println!("case04 passed");
}
