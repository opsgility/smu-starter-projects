//! SMU-RUST-700 Lesson 6 — lock-free counter with AtomicUsize.
//!
//! Exercises:
//! 1. Smoke test.
//! 2. Replace the `increment` todo!() with fetch_add + Relaxed.
//! 3. Benchmark against Arc<Mutex<usize>> and write up the result.

use std::sync::atomic::{AtomicUsize, Ordering};

pub struct Counter {
    value: AtomicUsize,
}

impl Counter {
    pub fn new() -> Self {
        Self { value: AtomicUsize::new(0) }
    }

    pub fn increment(&self) -> usize {
        todo!("Exercise 2: fetch_add(1, Ordering::Relaxed)")
    }

    pub fn get(&self) -> usize {
        self.value.load(Ordering::Relaxed)
    }
}

impl Default for Counter {
    fn default() -> Self { Self::new() }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::Arc;
    use std::collections::HashSet;

    #[test]
    fn increment_returns_pre_value() {
        let c = Counter::new();
        assert_eq!(c.increment(), 0);
        assert_eq!(c.increment(), 1);
        assert_eq!(c.get(), 2);
    }

    #[test]
    fn get_sees_increments() {
        let c = Counter::new();
        for _ in 0..100 { c.increment(); }
        assert_eq!(c.get(), 100);
    }

    #[test]
    fn many_threads_each_get_unique_ids() {
        let c = Arc::new(Counter::new());
        let per_thread = 500;
        let threads = 4;
        let handles: Vec<_> = (0..threads).map(|_| {
            let c = c.clone();
            std::thread::spawn(move || {
                let mut ids = Vec::new();
                for _ in 0..per_thread { ids.push(c.increment()); }
                ids
            })
        }).collect();
        let mut all = HashSet::new();
        for h in handles {
            for id in h.join().unwrap() {
                assert!(all.insert(id), "duplicate id: {}", id);
            }
        }
        assert_eq!(all.len(), threads * per_thread);
    }
}
