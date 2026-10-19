// case02: Function takes a Vec by value when a slice would do.
//
// EXPECTED ERROR: E0382 — borrow of moved value: `scores`.
// HINT: `sum_of(scores)` takes `scores` by value (`Vec<i32>`), which moves it
//       into the function. The caller cannot use `scores` after the call.
//
// FIX ME: change `sum_of` to accept a slice reference `&[i32]` and update
//         the call site to pass `&scores`. Slices are the idiomatic
//         parameter type for "read-only view into a sequence."
//
// Keep the `println!` that uses `scores` after the call — the whole point of
// the fix is that the caller still owns `scores` afterwards.

fn sum_of(v: Vec<i32>) -> i32 {
    v.iter().sum()
}

fn main() {
    let scores = vec![10, 20, 30, 40, 50];

    let total = sum_of(scores);

    println!("total  = {}", total);
    println!("scores = {:?}", scores);

    println!("case02 passed");
}
