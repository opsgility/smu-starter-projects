// EXPECTED ERROR: E0505 cannot move out of `v` because it is borrowed
// HINT: `first` holds a shared borrow of `v`. Then `move_vec(v)` tries to move v
//       into another function. The compiler says: "v is borrowed by first; you
//       can't move it while borrowed."
//       NLL fix: use `first` BEFORE the move, so the borrow has ended by the
//       time move_vec(v) runs. OR drop `first` explicitly. OR .clone() v so the
//       move takes a copy and leaves the borrowed one in place.

fn move_vec(v: Vec<i32>) {
    println!("moved vec has {} elements", v.len());
}

fn main() {
    let v = vec![10, 20, 30];
    let first = &v[0];

    // FIX ME: this line moves `v` while `first` is still borrowed from v.
    //         Reorder so first is used (and NLL-dropped) BEFORE this line.
    move_vec(v);

    println!("first was: {first}");
}
