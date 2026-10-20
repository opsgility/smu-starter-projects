// Drill 4 — RefCell behind Arc.
//
// This drill FAILS to compile on purpose. Fix: swap RefCell -> Mutex,
// borrow_mut() -> lock().unwrap().
//
// Expected error on `cargo build --bin drill04`:
//   error[E0277]: `RefCell<Vec<u32>>` cannot be shared between threads safely

use std::cell::RefCell;
use std::sync::Arc;
use std::thread;

fn main() {
    let v = Arc::new(RefCell::new(Vec::<u32>::new()));
    let mut handles = vec![];
    for id in 0..3u32 {
        let v = Arc::clone(&v);
        handles.push(thread::spawn(move || {
            for i in 0..100 {
                v.borrow_mut().push(id * 1000 + i);
            }
        }));
    }
    for h in handles { h.join().unwrap(); }
    println!("v.len() = {}", v.borrow().len());
}
