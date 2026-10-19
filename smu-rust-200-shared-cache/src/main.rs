// shared_cache starter — slow Fibonacci. Exercises add memoization + sharing.
//
// Run with: cargo run
// You'll see each Fibonacci call take exponentially longer. The exercises
// convert this to a memoized version using Rc<RefCell<HashMap>>.

use std::time::Instant;

fn fibonacci(n: u64) -> u64 {
    if n < 2 {
        return n;
    }
    fibonacci(n - 1) + fibonacci(n - 2)
}

fn main() {
    for n in [10u64, 20, 30, 35] {
        let start = Instant::now();
        let value = fibonacci(n);
        let elapsed = start.elapsed();
        println!("fib({n}) = {value} ({elapsed:?})");
    }
}
