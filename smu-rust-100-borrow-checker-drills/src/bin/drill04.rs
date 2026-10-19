// FIX ME: Make this program compile and print `first was 1` then `drill 04 passed`.
// EXPECTED ERROR: E0502 — cannot borrow `v` as mutable because it is also
//                 borrowed as immutable
// Hint: the immutable borrow `r` lives until its LAST use. Rust won't let
//       you take a `&mut v` while `r` is still alive. The smallest fix is
//       to reorder the lines so `r`'s last use (the println!) happens BEFORE
//       `v.push(4)`.

fn main() {
    let mut v = vec![1, 2, 3];
    let r = &v[0];
    v.push(4);
    println!("first was {r}");
    println!("drill 04 passed");
}
