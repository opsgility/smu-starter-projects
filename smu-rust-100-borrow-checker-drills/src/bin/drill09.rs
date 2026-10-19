// FIX ME: Make this program compile and print `data has 3 elements: [10, 20, 30]`
//         then `drill 09 passed`.
// EXPECTED ERROR: E0382 — use of moved value: `data`
// Hint: `length` takes `Vec<i32>` by VALUE — the call `length(data)` moves
//       the Vec into the function and `data` is no longer usable afterward.
//       Change `length` so it BORROWS the Vec instead of taking ownership:
//       `fn length(v: &Vec<i32>) -> usize` and pass `&data` at the call site.

fn length(v: Vec<i32>) -> usize {
    v.len()
}

fn main() {
    let data = vec![10, 20, 30];
    let n = length(data);
    println!("data has {n} elements: {data:?}");
    println!("drill 09 passed");
}
