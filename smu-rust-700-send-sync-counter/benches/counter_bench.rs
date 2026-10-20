//! Microbenchmark harness driven by src/bin/compare.rs.

use smu_rust_700_send_sync_counter::Counter;
use std::sync::{Arc, Mutex};
use std::time::{Duration, Instant};

pub fn bench_atomic(_threads: usize, _iterations: usize) -> Duration {
    todo!("Exercise 3: spawn N threads each calling counter.increment() M times")
}

pub fn bench_mutex(_threads: usize, _iterations: usize) -> Duration {
    todo!("Exercise 3: spawn N threads each incrementing an Arc<Mutex<usize>>")
}
