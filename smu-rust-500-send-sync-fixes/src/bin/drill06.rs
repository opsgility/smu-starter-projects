// Drill 6 — compound struct with Rc<RefCell<_>> field.
//
// This drill FAILS to compile on purpose. Fix: Rc<RefCell<HashMap>>
// becomes Arc<Mutex<HashMap>>. The whole State struct becomes Send+Sync
// by marker-trait propagation.
//
// Expected error on `cargo build --bin drill06`:
//   error[E0277]: `Rc<RefCell<HashMap<String, u32>>>` cannot be sent between threads safely
//   note: required because it appears within the type `State`

use std::cell::RefCell;
use std::collections::HashMap;
use std::rc::Rc;
use std::sync::Arc;
use std::thread;

#[derive(Clone)]
struct Config {
    name: String,
}

struct State {
    config: Arc<Config>,
    cache: Rc<RefCell<HashMap<String, u32>>>,
}

fn main() {
    let state = State {
        config: Arc::new(Config { name: String::from("cfg") }),
        cache: Rc::new(RefCell::new(HashMap::new())),
    };

    let h = thread::spawn(move || {
        for i in 0..10 {
            state.cache.borrow_mut().insert(format!("k{i}"), i);
        }
        println!("thread used config {}", state.config.name);
        state
    });
    let state = h.join().unwrap();
    println!("cache has {} keys", state.cache.borrow().len());
}
