// EXPECTED ERROR: E0505 — cannot move out of `v` because it is borrowed
// HINT: `first` is a shared borrow of `v[0]` that must stay alive until its
//       last use. The code then tries to move `v` into `move_vec` while
//       `first` is still used. The idiomatic fix is to reorder — use (and
//       print) `first` BEFORE handing `v` to `move_vec`.
// FIX ME: Make this compile.

fn move_vec(v: Vec<i32>) {
    println!("moved vec has {} elements", v.len());
}

fn main() {
    let v = vec![10, 20, 30];

    let first = &v[0];
    move_vec(v);
    println!("first was: {first}");
}
