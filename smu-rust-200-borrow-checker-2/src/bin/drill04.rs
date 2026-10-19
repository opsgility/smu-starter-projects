// EXPECTED ERROR: E0499 cannot borrow `v` as mutable more than once at a time
// HINT: `a` is a &mut v. `b` is another &mut v while `a` is still alive. The
//       compiler flags b. BUT: if `a` is finished BEFORE `b` is taken, NLL ends
//       a's borrow at its last use and b is fine. Reorder the uses — do
//       everything with `a` first, then take `b`.

fn main() {
    let mut v = vec![1, 2, 3];

    let a = &mut v;
    let b = &mut v;

    // FIX ME: both `a` and `b` are live here. Reorder so a's `push` happens
    //         BEFORE taking `b`. NLL will then end a's borrow at its last use.
    a.push(10);
    b.push(20);

    println!("v = {v:?}");
}
