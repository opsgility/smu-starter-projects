#[derive(Debug, Clone)]
pub struct Record {
    pub source_id: u32,
    pub value: f64,
}

#[derive(Debug, Clone, Default, PartialEq)]
pub struct Stats {
    pub count: u64,
    pub sum: f64,
    pub min: f64,
    pub max: f64,
}

impl Stats {
    pub fn accumulate(&mut self, v: f64) {
        if self.count == 0 {
            self.min = v;
            self.max = v;
        } else {
            if v < self.min { self.min = v; }
            if v > self.max { self.max = v; }
        }
        self.count += 1;
        self.sum += v;
    }
    pub fn merge(&mut self, other: Stats) {
        if other.count == 0 { return; }
        if self.count == 0 {
            *self = other;
            return;
        }
        self.count += other.count;
        self.sum += other.sum;
        if other.min < self.min { self.min = other.min; }
        if other.max > self.max { self.max = other.max; }
    }
}

pub fn generate_records(n: usize) -> Vec<Record> {
    (0..n)
        .map(|i| Record {
            source_id: (i % 20) as u32,
            value: (i as f64) * 0.5 + 0.01,
        })
        .collect()
}

pub fn par_merge_stats(
    mut a: std::collections::HashMap<u32, Stats>,
    b: std::collections::HashMap<u32, Stats>,
) -> std::collections::HashMap<u32, Stats> {
    for (k, s_b) in b {
        a.entry(k).or_default().merge(s_b);
    }
    a
}
