// lazy-eager starter — fill in each exercise.
//
// The two sum functions below are stubs. Across the exercises you'll:
//   - Fill `wasteful_sum` with the collect-then-sum version (Ex 2).
//   - Fill `direct_sum` with the single-pass version (Ex 2).
//   - Measure the time ratio between them at different N values (Ex 3).
//   - Write a `needs_vec` that MUST materialize (Ex 4).
//   - Write a borrow-into-collect example (Ex 5, optional).

use std::time::Instant;

/// Build a Vec of i32 values from 0..n for use as benchmark input.
fn gen_vec(n: usize) -> Vec<i32> {
    (0..n as i32).collect()
}

/// Collect-then-sum version. Fill this in during Exercise 2.
#[allow(dead_code)]
fn wasteful_sum(_v: &[i32]) -> i32 {
    todo!("Ex 2: filter even numbers, collect into a Vec, then sum")
}

/// Single-pass version. Fill this in during Exercise 2.
#[allow(dead_code)]
fn direct_sum(_v: &[i32]) -> i32 {
    todo!("Ex 2: filter even numbers and sum in one pass")
}

/// Lightweight benchmarking helper. Captures a label, calls `f`, prints the
/// elapsed time in milliseconds, and returns whatever `f` returned.
#[allow(dead_code)]
fn time<F, R>(label: &str, f: F) -> R
where
    F: FnOnce() -> R,
{
    let start = Instant::now();
    let result = f();
    let elapsed = start.elapsed();
    println!("{label:20} {elapsed:?}");
    result
}

fn main() {
    println!("lazy-eager starter — fill in each exercise");
    let v = gen_vec(10);
    println!("gen_vec(10) first 5 = {:?}", &v[..5]);
}
