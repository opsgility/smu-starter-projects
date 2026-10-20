// Drill 1 — Rc across threads.
//
// This drill FAILS to compile on purpose. Fix: Rc -> Arc.
//
// Expected error on `cargo build --bin drill01`:
//   error[E0277]: `Rc<i32>` cannot be sent between threads safely

use std::rc::Rc;
use std::thread;

fn main() {
    let shared = Rc::new(42i32);
    let clone = Rc::clone(&shared);
    let handle = thread::spawn(move || {
        println!("worker sees {}", *clone);
    });
    handle.join().unwrap();
    println!("shared = {}", *shared);
}
