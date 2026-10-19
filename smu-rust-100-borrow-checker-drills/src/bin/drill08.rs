// FIX ME: Make this program compile and print the sorted names then `drill 08 passed`.
// EXPECTED ERROR: E0596 — cannot borrow `names` as mutable
// Hint: `Vec::sort` takes `&mut self` — the Vec needs to be mutable at the
//       `let` site. Same shape as drill 03 but with a different method.

fn main() {
    let names = vec![
        String::from("gamma"),
        String::from("alpha"),
        String::from("beta"),
    ];
    names.sort();
    println!("{names:?}");
    println!("drill 08 passed");
}
