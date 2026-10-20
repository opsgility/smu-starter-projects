// EXPECTED ERROR: E0382 — borrow of moved value: `scores`
// HINT: `.into_iter()` takes ownership of each element and drops the Vec
//       header. After `.collect()`, `scores` is gone and the follow-up
//       `scores.len()` fails. The idiomatic fix is `.iter()` instead —
//       `|x| x * 2` works unchanged because arithmetic auto-derefs `&i32`.
// FIX ME: Make this program compile and print `case05 passed`.

fn main() {
    let scores = vec![1, 2, 3, 4];
    let doubled: Vec<i32> = scores.into_iter().map(|x| x * 2).collect();

    println!("doubled = {doubled:?}");
    println!("original len = {}", scores.len());
    println!("case05 passed");
}
