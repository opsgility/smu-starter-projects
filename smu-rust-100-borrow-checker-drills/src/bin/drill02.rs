// FIX ME: Make this program compile and print `drill 02 passed (n = 2)`.
// EXPECTED ERROR: E0384 — cannot assign twice to immutable variable `n`
// Hint: `let` makes bindings immutable by default. There is one keyword
//       you add after `let` that lets you reassign the same binding.

fn main() {
    let n = 1;
    n = 2;
    println!("drill 02 passed (n = {n})");
}
