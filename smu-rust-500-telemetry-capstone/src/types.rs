#[derive(Debug, Clone)]
pub struct RawPacket {
    pub source_id: u32,
    pub seq: u32,
    pub payload: Vec<u8>,
}

#[derive(Debug, Clone)]
pub struct Reading {
    pub source_id: u32,
    pub seq: u32,
    pub ts_unix_ms: u64,
    pub value: f64,
}

#[derive(Debug, Clone)]
pub struct Station {
    pub id: u32,
    pub last_seen_unix_ms: u64,
}

impl Station {
    pub fn new(id: u32) -> Self {
        Self { id, last_seen_unix_ms: 0 }
    }
}

#[derive(Debug, Clone, Default)]
pub struct WindowStats {
    pub count: u64,
    pub sum: f64,
}

impl WindowStats {
    pub fn accumulate(&mut self, r: &Reading) {
        self.count += 1;
        self.sum += r.value;
    }
    pub fn merge(&mut self, other: WindowStats) {
        self.count += other.count;
        self.sum += other.sum;
    }
}

pub fn merge_window_stats(
    mut a: std::collections::HashMap<u32, WindowStats>,
    b: std::collections::HashMap<u32, WindowStats>,
) -> std::collections::HashMap<u32, WindowStats> {
    for (k, s_b) in b {
        a.entry(k).or_default().merge(s_b);
    }
    a
}

pub fn parse(raw: &RawPacket) -> Option<Reading> {
    if raw.payload.len() < 8 {
        return None;
    }
    let value_bytes: [u8; 8] = raw.payload[..8].try_into().ok()?;
    Some(Reading {
        source_id: raw.source_id,
        seq: raw.seq,
        ts_unix_ms: now_unix_ms(),
        value: f64::from_le_bytes(value_bytes),
    })
}

fn now_unix_ms() -> u64 {
    use std::time::{SystemTime, UNIX_EPOCH};
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .map(|d| d.as_millis() as u64)
        .unwrap_or(0)
}
