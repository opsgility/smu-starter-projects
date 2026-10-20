// Three starter APIs you refactor:
//   EX 2 → fn total: widen from &Vec<i32> to IntoIterator<Item = i32>
//   EX 3 → fn repeated: switch from Vec<String> return to impl Iterator<Item = String>
//   EX 4 → impl Iterator for Fibonacci + newtype iterator pattern
//   EX 5 (optional) → factory fn returning Fibonacci

fn total(nums: &Vec<i32>) -> i32 {
    let mut sum = 0;
    for n in nums {
        sum += n;
    }
    sum
}

fn repeated(s: &str, n: usize) -> Vec<String> {
    let mut out = Vec::new();
    for _ in 0..n {
        out.push(s.to_string());
    }
    out
}

pub struct Fibonacci {
    pub a: u64,
    pub b: u64,
}

impl Fibonacci {
    pub fn new() -> Self {
        Fibonacci { a: 0, b: 1 }
    }
}

fn main() {
    let numbers = vec![1, 2, 3, 4, 5];
    println!("total(&numbers) = {}", total(&numbers));

    let words = repeated("rust", 3);
    println!("repeated(\"rust\", 3) = {:?}", words);

    let fib = Fibonacci::new();
    println!("fib state: a={}, b={}", fib.a, fib.b);

    // Exercise 4 — uncomment once impl Iterator for Fibonacci exists:
    // let fibs: Vec<u64> = Fibonacci::new().take(10).collect();
    // println!("first 10 fibs = {:?}", fibs);
}
