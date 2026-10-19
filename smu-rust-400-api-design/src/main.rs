// api-design starter — iterator-friendly API patterns.
//
// Across the exercises you'll refactor three APIs:
//   * EX 2: `total` -> accept any IntoIterator<Item = i32>
//   * EX 3: `repeated` -> return an impl Iterator<Item = String>, lazy
//   * EX 4: wrap `Fibonacci` in the newtype iterator pattern
//
// Everything compiles and runs as-is. Your job is to tighten the shape of
// each API, not fix bugs.

/// Sum every element of a Vec<i32>. Restrictive — only accepts a Vec.
///
/// EX 2: refactor to `fn total<I: IntoIterator<Item = i32>>(iter: I) -> i32`.
fn total(v: &Vec<i32>) -> i32 {
    let mut sum = 0;
    for &x in v {
        sum += x;
    }
    sum
}

/// Build a Vec of n copies of s. Eager — allocates upfront.
///
/// EX 3: refactor to return `impl Iterator<Item = String> + '_` using
/// `std::iter::repeat(s.to_string()).take(n)`.
fn repeated(s: &str, n: usize) -> Vec<String> {
    let mut out = Vec::with_capacity(n);
    for _ in 0..n {
        out.push(s.to_string());
    }
    out
}

/// Fibonacci state machine. Fields are in place and `new` works, but no
/// `Iterator` impl yet — EX 4 adds it.
pub struct Fibonacci {
    a: u64,
    b: u64,
}

impl Fibonacci {
    pub fn new() -> Self {
        Fibonacci { a: 0, b: 1 }
    }
}

fn main() {
    // --- total (EX 2) ---
    let numbers = vec![1, 2, 3, 4, 5];
    println!("total(&numbers) = {}", total(&numbers));

    // --- repeated (EX 3) ---
    let words = repeated("rust", 3);
    println!("repeated(\"rust\", 3) = {:?}", words);

    // --- Fibonacci (EX 4) ---
    // Will come alive once you add `impl Iterator for Fibonacci` in EX 4.
    // Uncomment after you implement the trait:
    //
    //     let fibs: Vec<u64> = Fibonacci::new().take(10).collect();
    //     println!("first 10 fibs = {:?}", fibs);
    let fib = Fibonacci::new();
    println!("fib state: a={}, b={}", fib.a, fib.b);
}
