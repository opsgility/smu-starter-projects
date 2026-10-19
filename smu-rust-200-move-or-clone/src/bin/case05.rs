// case05: `into_iter()` moved the Vec; we can't use it after.
//
// EXPECTED ERROR: E0382 — borrow of moved value: `scores`.
// HINT: `.into_iter()` consumes the collection (takes ownership of each
//       element). After the chain, `scores` no longer owns anything, so the
//       `{:?}` print at the end fails.
//
// FIX ME: swap `.into_iter()` for `.iter()`. The chain then yields `&i32`
//         instead of `i32`, so `|x| x * 2` becomes `|x| x * 2` operating on
//         `&i32` — add a single `*` to deref inside the closure (`|x| *x * 2`),
//         OR keep the chain as-is and let auto-deref in arithmetic resolve it.
//         The important choice: borrow (`iter`) vs consume (`into_iter`).

fn main() {
    let scores = vec![10, 20, 30, 40];

    let doubled: Vec<i32> = scores.into_iter().map(|x| x * 2).collect();

    println!("original = {:?}", scores);
    println!("doubled  = {:?}", doubled);

    println!("case05 passed");
}
