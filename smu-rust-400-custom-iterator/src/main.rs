#[allow(dead_code)]
pub struct Fibonacci {
    pub a: u64,
    pub b: u64,
}

impl Fibonacci {
    #[allow(dead_code)]
    pub fn new() -> Self {
        Fibonacci { a: 0, b: 1 }
    }
}

#[allow(dead_code)]
pub struct Words<'a> {
    pub source: &'a str,
    pub cursor: usize,
}

impl<'a> Words<'a> {
    #[allow(dead_code)]
    pub fn new(source: &'a str) -> Self {
        Words { source, cursor: 0 }
    }
}

fn main() {
    println!("custom-iterator starter — see README.md for the exercises.\n");

    // Exercise 2 — uncomment:
    // let first_ten: Vec<u64> = Fibonacci::new().take(10).collect();
    // println!("first ten Fibonacci: {first_ten:?}");

    // Exercise 3 — uncomment:
    // let text = "  one   two three   ";
    // let tokens: Vec<&str> = Words::new(text).collect();
    // println!("tokens: {tokens:?}");

    // Exercise 4 — uncomment (requires Exercise 3's Words impl):
    // let total = Words::new("alpha beta gamma delta").count();
    // println!("word count: {total}");
}
