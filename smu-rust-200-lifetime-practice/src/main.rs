// Lifetime annotations in practice — Course 638 Lesson 6 paired HOL
//
// Three of the four fns + the struct below are deliberately broken so the
// Rust compiler asks you to apply what Lesson 6 taught about lifetimes:
//
//   - `longest` returns a reference, has 2 inputs, no `&self`:
//     elision rule 2/3 don't apply → needs explicit `'a` annotations.
//   - `first_word` returns a reference, has 1 input, no `&self`:
//     elision rule 2 applies → NO annotations needed.
//     (Exercise 3 asks you to document which rule covers it.)
//   - `Excerpt` struct holds a reference, needs `'a` on the struct.
//   - `use_excerpt` is OK AS A SIGNATURE once `Excerpt<'a>` is fixed —
//     elision links `Excerpt<'a>` → `&'a str` output automatically.
//
// You'll start by running `cargo build`, then fix each item in order.

fn longest(a: &str, b: &str) -> &str {
    if a.len() > b.len() {
        a
    } else {
        b
    }
}

fn first_word(s: &str) -> &str {
    s.split_whitespace().next().unwrap_or("")
}

struct Excerpt {
    source: &str,
}

fn use_excerpt(e: Excerpt) -> &str {
    e.source
}

fn main() {
    let a = String::from("short");
    let b = String::from("much longer than short");
    println!("longest = {}", longest(&a, &b));

    let sentence = String::from("the quick brown fox");
    println!("first word = {}", first_word(&sentence));

    let paragraph = String::from("Rust lifetimes are compile-time regions, not runtime durations.");
    let e = Excerpt { source: &paragraph };
    println!("excerpt = {}", use_excerpt(e));
}
