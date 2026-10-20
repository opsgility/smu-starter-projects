// EXPECTED ERROR: E0382 — borrow of moved value: `scores`
// HINT: `sum_of(v: Vec<i32>)` takes ownership of the Vec. After the first
//       call, `scores` is gone, so the follow-up `println!("len = {}",
//       scores.len())` fails. The idiomatic fix is to make `sum_of` take a
//       slice (`&[i32]`) so no ownership transfer happens.
// FIX ME: Make this program compile and print `case02 passed`.

fn sum_of(v: Vec<i32>) -> i32 {
    v.iter().sum()
}

fn main() {
    let scores = vec![10, 20, 30, 40];
    let total = sum_of(scores);
    println!("total = {total}");
    println!("len = {}", scores.len());
    println!("case02 passed");
}
