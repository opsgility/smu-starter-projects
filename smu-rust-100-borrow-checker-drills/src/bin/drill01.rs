// FIX ME: Make this program compile and print `drill 01 passed`.
// EXPECTED ERROR: E0382 — use of moved value: `s`
// Hint: assigning a String to a new binding MOVES ownership — after
//       `let _t = s;`, the name `s` is no longer usable. Either clone
//       the String so both bindings own their own copy, or avoid the
//       assignment to `_t` altogether.

fn main() {
    let s = String::from("drill 01");
    let _t = s;
    println!("{s} passed");
}
