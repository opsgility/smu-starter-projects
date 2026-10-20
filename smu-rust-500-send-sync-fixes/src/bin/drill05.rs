// Drill 5 — MutexGuard across a thread handoff.
//
// This drill FAILS to compile on purpose. Fix: clone the value out of
// the guard BEFORE spawning, drop the guard, send only the owned clone.
//
// Expected error on `cargo build --bin drill05`:
//   error[E0277]: `MutexGuard<'_, String>` cannot be sent between threads safely

use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let m = Arc::new(Mutex::new(String::from("hello")));
    let guard = m.lock().unwrap();
    let h = thread::spawn(move || {
        println!("worker saw: {}", &*guard);
    });
    h.join().unwrap();
}
