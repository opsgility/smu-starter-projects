#[derive(Debug, Clone)]
pub struct Record {
    pub source_id: u32,
    pub value: f64,
}

pub fn generate_records(n: usize) -> Vec<Record> {
    (0..n)
        .map(|i| Record {
            source_id: (i % 20) as u32,
            value: (i as f64) * 0.5 + 0.01,
        })
        .collect()
}
