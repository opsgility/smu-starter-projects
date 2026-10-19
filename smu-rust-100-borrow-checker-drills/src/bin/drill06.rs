// FIX ME: Make this program compile and print the borrowed Vec then `drill 06 passed`.
// EXPECTED ERROR: E0505 — cannot move out of `v` because it is borrowed
// Hint: `r` is an immutable borrow of `v`. You can't MOVE `v` into
//       `_moved` while `r` is still alive (its last use is the println!).
//       Reorder so the borrow's last use happens BEFORE the move.

fn main() {
    let v = vec![String::from("a"), String::from("b")];
    let r = &v;
    let _moved = v;
    println!("{r:?}");
    println!("drill 06 passed");
}
