use std::time::Instant;

// Exponential Fibonacci — no memoization. Exercise 2 rewrites this to use
// Rc<RefCell<HashMap>> so repeated subproblems are cached.
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
