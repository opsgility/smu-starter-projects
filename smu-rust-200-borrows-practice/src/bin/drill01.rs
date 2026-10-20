// drill01 — shared borrow then exclusive borrow, no overlap (NLL).
//
// This compiles as shipped. In Exercise 2 you uncomment the TRY block below
// to see E0502: the final println! keeps the shared borrow alive past the
// mutable borrow attempt.

fn sum_all(nums: &Vec<i32>) -> i32 {
    nums.iter().sum()
}

fn push_one(nums: &mut Vec<i32>, v: i32) {
    nums.push(v);
}

fn main() {
    let mut nums = vec![1, 2, 3, 4, 5];

    let total = sum_all(&nums);
    println!("sum before push = {total}");

    push_one(&mut nums, 99);

    let total = sum_all(&nums);
    println!("sum after push  = {total}");

    // TRY in Exercise 2 — uncomment this block to force E0502.
    // let r = &nums;
    // push_one(&mut nums, 7);
    // println!("peek r = {:?}", r);

    println!("drill01 passed");
}
