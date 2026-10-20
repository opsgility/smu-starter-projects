mod types;
use types::{generate_records, Record};

use std::time::Instant;

fn serial_sum(records: &[Record]) -> f64 {
    records.iter().map(|r| r.value).sum()
}

fn main() {
    let records = generate_records(1_000_000);
    let start = Instant::now();
    let sum = serial_sum(&records);
    let took = start.elapsed();
    println!("serial: n={} sum={sum:.2} (took {took:?})", records.len());
}
