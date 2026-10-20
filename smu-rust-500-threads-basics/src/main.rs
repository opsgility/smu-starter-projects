use std::time::Instant;

pub fn generate_data(n: usize) -> Vec<u64> {
    (0..n as u64).collect()
}

pub fn sum_slice(data: &[u64]) -> u64 {
    data.iter().sum()
}

fn main() {
    let data = generate_data(1_000_000);
    let start = Instant::now();
    let total = sum_slice(&data);
    let took = start.elapsed();
    println!("serial sum = {total}  (took {took:?})");
}
