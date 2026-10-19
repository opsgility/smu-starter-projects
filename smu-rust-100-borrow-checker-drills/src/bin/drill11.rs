// FIX ME: Make this program compile and print `drill 11 passed`.
// EXPECTED ERROR: E0597 — `temp` does not live long enough
// Hint: `temp` is declared inside the inner `{ ... }` block, so it DROPS the
//       moment the block ends. `s = &temp` makes `s` a reference INTO temp —
//       after the block closes, `s` would dangle. Simplest fix: don't take a
//       reference. Bind the owned String directly in `s`.

fn main() {
    let s;
    {
        let temp = String::from("drill 11");
        s = &temp;
    }
    println!("{s} passed");
}
