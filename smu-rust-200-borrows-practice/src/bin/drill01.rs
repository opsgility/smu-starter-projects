// drill01 — shared vs mutable borrows, and the E0502 break
//
// EXPECTED: this file compiles and runs cleanly. In exercise 2 you intentionally
// break it by uncommenting the TRY block below.
//
// Pattern: pass `&Vec<i32>` to a reader fn (returns the sum) and `&mut Vec<i32>`
// to a writer fn (pushes a value). Each borrow is in its own statement, so the
// shared and exclusive borrows never overlap — the borrow checker is happy.

fn sum_all(v: &Vec<i32>) -> i32 {
    v.iter().sum()
}

fn push_one(v: &mut Vec<i32>, x: i32) {
    v.push(x);
}

fn main() {
    let mut nums = vec![1, 2, 3, 4, 5];

    // Reader fn takes a shared borrow. Borrow ends at the end of this line.
    let total = sum_all(&nums);
    println!("sum before push = {total}");

    // Writer fn takes an exclusive borrow. The previous shared borrow is long
    // gone (NLL — borrow ends at last use), so this is fine.
    push_one(&mut nums, 99);

    // Fresh shared borrow after the writer returns.
    let total2 = sum_all(&nums);
    println!("sum after push  = {total2}");

    println!("drill01 passed");

    // TRY in Exercise 2 — uncomment this line to see E0502 "cannot borrow as
    // mutable because it is also borrowed as immutable":
    //
    //     let r = &nums;
    //     push_one(&mut nums, 7);
    //     println!("peek r = {:?}", r);
    //
    // Rust refuses because `r` is still alive at the push_one call. The fix:
    // use `r` BEFORE the push, so the borrow ends.
}
