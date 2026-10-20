// Drill 2 — raw pointer.
//
// This drill FAILS to compile on purpose. Fix: swap *mut i32
// for an Arc<Mutex<i32>>.
//
// Expected error on `cargo build --bin drill02`:
//   error[E0277]: `*mut i32` cannot be sent between threads safely

use std::thread;

fn main() {
    let mut value = 0i32;
    let ptr: *mut i32 = &mut value;
    let mut handles = vec![];
    for _ in 0..10 {
        handles.push(thread::spawn(move || {
            unsafe { *ptr += 100; }
        }));
    }
    for h in handles { h.join().unwrap(); }
    println!("final = {}", value);
}
