// FIX ME: Make this program compile and print `alpha` then `drill 05 passed`.
// EXPECTED ERROR: E0507 — cannot move out of index of `Vec<String>`
// Hint: `v[0]` tries to MOVE the String out of the Vec — but that would leave
//       a hole where the first element used to be, so Rust won't allow it.
//       Two options: clone it into a new owned String, or take a reference
//       (`&v[0]`) if you only need to read.

fn main() {
    let v = vec![String::from("alpha")];
    let s = v[0];
    println!("{s}");
    println!("drill 05 passed");
}
