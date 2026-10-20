// Drill 3 — Cell behind Arc.
//
// This drill FAILS to compile on purpose. Fix: swap Cell -> Mutex
// (or AtomicI32).
//
// Expected error on `cargo build --bin drill03`:
//   error[E0277]: `Cell<i32>` cannot be shared between threads safely

use std::cell::Cell;
use std::sync::Arc;
use std::thread;

fn main() {
    let counter = Arc::new(Cell::new(0i32));
    let mut handles = vec![];
    for _ in 0..3 {
        let c = Arc::clone(&counter);
        handles.push(thread::spawn(move || {
            for _ in 0..100 {
                c.set(c.get() + 1);
            }
        }));
    }
    for h in handles { h.join().unwrap(); }
    println!("counter = {}", counter.get());
}
