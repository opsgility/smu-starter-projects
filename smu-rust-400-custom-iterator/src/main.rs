// Custom iterator starter — Course 4 Lesson 3 paired HOL.
//
// You will add `impl Iterator for Fibonacci` + `impl Iterator for Words<'a>`
// as you work through the exercises. The structs below are declared but
// have no Iterator implementation yet — that's your job.

pub struct Fibonacci {
    pub a: u64,
    pub b: u64,
}

impl Fibonacci {
    pub fn new() -> Self {
        Fibonacci { a: 0, b: 1 }
    }
}

pub struct Words<'a> {
    pub source: &'a str,
    pub cursor: usize,
}

impl<'a> Words<'a> {
    pub fn new(source: &'a str) -> Self {
        Words { source, cursor: 0 }
    }
}

fn main() {
    println!("custom-iterator starter — see README.md for the exercises.");
    println!();

    // EX 2 will enable this once `impl Iterator for Fibonacci` is in place:
    // let first_ten: Vec<u64> = Fibonacci::new().take(10).collect();
    // println!("first ten Fibonacci: {first_ten:?}");

    // EX 3 will enable this once `impl Iterator for Words<'_>` is in place:
    // let text = "  one   two three   ";
    // let tokens: Vec<&str> = Words::new(text).collect();
    // println!("tokens: {tokens:?}");

    // EX 5 (optional) will add a `fibonacci_closure()` fn built from
    // std::iter::from_fn and compare it to the struct form.
}
