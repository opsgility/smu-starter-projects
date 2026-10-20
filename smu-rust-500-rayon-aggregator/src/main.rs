use rust_concurrent_rayon_aggregator::{generate_records, Record, Stats};
use std::collections::HashMap;
use std::time::Instant;

fn serial_aggregate(records: &[Record]) -> HashMap<u32, Stats> {
    records.iter().fold(HashMap::new(), |mut acc, r| {
        acc.entry(r.source_id).or_default().accumulate(r.value);
        acc
    })
}

fn main() {
    let records = generate_records(1_000_000);
    let start = Instant::now();
    let serial = serial_aggregate(&records);
    let took = start.elapsed();
    println!("serial: {} source groups, total count={} (took {took:?})",
        serial.len(),
        serial.values().map(|s| s.count).sum::<u64>());
}
