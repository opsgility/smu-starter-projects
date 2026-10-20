use crate::types::RawPacket;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::time::{Duration, Instant};

pub struct MockFeed {
    emitted: AtomicUsize,
    cap: usize,
    start: Instant,
    rate_per_sec: usize,
}

impl MockFeed {
    pub fn new(rate_per_sec: usize) -> Self {
        Self {
            emitted: AtomicUsize::new(0),
            cap: rate_per_sec * 10,
            start: Instant::now(),
            rate_per_sec,
        }
    }

    pub fn next_packet(&self) -> Option<RawPacket> {
        let n = self.emitted.fetch_add(1, Ordering::Relaxed);
        if n >= self.cap { return None; }

        let elapsed_secs = self.start.elapsed().as_secs_f64();
        let allowed = (elapsed_secs * self.rate_per_sec as f64) as usize;
        if n > allowed {
            std::thread::sleep(Duration::from_micros(50));
        }

        let source_id = (n as u32) % 20;
        let value: f64 = 100.0 + (n as f64) * 0.1;
        let mut payload = Vec::with_capacity(16);
        payload.extend_from_slice(&value.to_le_bytes());
        payload.extend_from_slice(&(n as u64).to_le_bytes());

        Some(RawPacket {
            source_id,
            seq: n as u32,
            payload,
        })
    }

    pub fn next_packet_timeout(&self, _timeout: Duration) -> Option<RawPacket> {
        self.next_packet()
    }
}
