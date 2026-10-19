// EXPECTED ERROR: E0384 cannot assign twice to immutable variable
// HINT: `total` is bound with `let total` (immutable). Later the code tries
//       `total += ...`. The fix is `let mut total = 0;` at the binding — NOT
//       at the assignment line. Watch out: there's a `let total = 0;` AND a
//       separate `let total = ...` shadow earlier; the shadow is irrelevant.
//       Fix the SECOND `let total = 0` to `let mut total = 0`.

fn main() {
    let total = String::from("<initial>");
    println!("intro: {total}");

    let total = 0;

    // FIX ME: `total` here is the i32 bound on the previous line. That binding
    //         is immutable. Change it to `let mut total = 0;`.
    for n in 1..=5 {
        total += n;
    }

    println!("sum 1..=5 = {total}");
}
