// FIX ME: Make this program compile and print the vector then `drill 03 passed`.
// EXPECTED ERROR: E0596 — cannot borrow `v` as mutable, as it is not declared
//                 as mutable
// Hint: `Vec::push` takes `&mut self` — the Vec itself has to be declared
//       mutable at the `let` site before you can mutate it.

fn main() {
    let v = vec![1, 2];
    v.push(3);
    println!("{v:?}");
    println!("drill 03 passed");
}
