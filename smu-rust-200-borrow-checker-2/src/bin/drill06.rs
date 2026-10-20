// EXPECTED ERROR: E0384 — cannot assign twice to immutable variable `total`
// HINT: There are two `let total = ...` lines. The compiler points at the
//       loop body, but the fix is at the BINDING the loop mutates — change
//       the SECOND `let total = 0;` to `let mut total = 0;`.
// FIX ME: Make this compile.

fn main() {
    let total = "<initial>";
    println!("intro: {total}");

    let total = 0;
    for n in 1..=5 {
        total += n;
    }
    println!("sum 1..=5 = {total}");
}
