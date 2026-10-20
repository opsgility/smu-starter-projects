// EXPECTED ERROR: E0596 — cannot borrow `self.count` as mutable, as it is
//                          behind a `&` reference
// HINT: `increment(&self)` takes a shared reference but mutates. Fix is at
//       the METHOD DEFINITION: change to `&mut self`. Then the binding in
//       main must be `let mut counter = ...`.
// FIX ME: Make this compile.

struct Counter {
    count: i32,
}

impl Counter {
    fn new() -> Self {
        Counter { count: 0 }
    }

    fn increment(&self) {
        self.count += 1;
    }
}

fn main() {
    let counter = Counter::new();
    counter.increment();
    counter.increment();
    println!("count = {}", counter.count);
}
