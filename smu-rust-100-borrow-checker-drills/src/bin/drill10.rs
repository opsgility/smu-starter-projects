// FIX ME: Make this program compile and print `[1, 2, 3, 4, 5]` then `drill 10 passed`.
// EXPECTED ERROR: E0499 — cannot borrow `v` as mutable more than once at a time
// Hint: `r1` and `r2` both try to hold a `&mut v` at the same time. Only one
//       active mutable borrow is allowed. The simplest fix: finish using `r1`
//       (its last .push call) BEFORE taking `r2`, so the first borrow is
//       already dead when the second starts.

fn main() {
    let mut v = vec![1, 2, 3];
    let r1 = &mut v;
    let r2 = &mut v;
    r1.push(4);
    r2.push(5);
    println!("{v:?}");
    println!("drill 10 passed");
}
