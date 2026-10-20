use std::time::Instant;

// Exercise 2 fills both sum stubs and times them at N = 1,000,000.
// Exercise 3 sweeps across input sizes and records the ratio.
// Exercise 4 adds needs_vec — showing when .collect() is required.
// Exercise 5 (optional) adds Collect-for-borrow-lifetime demo.
//
// Build with --release when timing — debug optimizer barely runs.

pub fn gen_vec(n: usize) -> Vec<i32> {
    (0..n as i32).collect()
}

pub fn time<T>(label: &str, f: impl FnOnce() -> T) -> T {
    let start = Instant::now();
    let result = f();
    let elapsed = start.elapsed();
    println!("{label:<20} {:>8.1}ms", elapsed.as_secs_f64() * 1000.0);
    result
}

#[allow(dead_code)]
pub fn wasteful_sum(_v: &[i32]) -> i32 {
    todo!("Exercise 2: collect filtered values into a Vec, then sum")
}

#[allow(dead_code)]
pub fn direct_sum(_v: &[i32]) -> i32 {
    todo!("Exercise 2: single-pass filter + sum, no intermediate collect")
}

fn main() {
    println!("lazy-eager starter — fill in each exercise");

    let preview = gen_vec(10);
    let first_five: Vec<i32> = preview.iter().take(5).copied().collect();
    println!("gen_vec(10) first 5 = {first_five:?}");
}
