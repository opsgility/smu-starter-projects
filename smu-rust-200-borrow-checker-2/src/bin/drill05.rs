// EXPECTED ERROR: E0596 cannot borrow `*self` as mutable, as it is behind a `&` reference
// HINT: The method `increment` takes `&self` but tries to mutate `self.count`.
//       The fix is NOT at the call site — it's at the METHOD DEFINITION.
//       Change `fn increment(&self)` to `fn increment(&mut self)`.
//       Then the binding of `counter` in main() must also be `let mut counter`.

struct Counter {
    count: u32,
}

impl Counter {
    fn new() -> Self {
        Counter { count: 0 }
    }

    // FIX ME: this method mutates self.count but declares &self (shared). Change
    //         to &mut self.
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
