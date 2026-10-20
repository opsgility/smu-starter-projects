// EXPECTED ERROR: E0594 — cannot assign to `self.count`, which is behind a
//                          `&` reference. (Older Rust emitted E0596 for the
//                          same shape — the help block names the fix either
//                          way: `&mut self`.)
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
