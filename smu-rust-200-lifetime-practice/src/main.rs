// This starter ships three deliberately broken items. `cargo build` prints
// three error blocks. You fix them across Exercises 2 and 4.
//
//   - `longest`  — missing lifetime annotation on two input references.
//   - `Excerpt`  — struct holds a reference field without a lifetime param.
//   - `use_excerpt` — downstream fallout from the struct error; disappears
//                     once the struct is fixed (elision covers the function).
//
// `first_word` compiles with no annotations — elision rules do the work.
// Exercise 3 asks you to add a comment naming the rule.

fn longest(a: &str, b: &str) -> &str {
    if a.len() >= b.len() { a } else { b }
}

fn first_word(s: &str) -> &str {
    let bytes = s.as_bytes();
    for (i, &b) in bytes.iter().enumerate() {
        if b == b' ' {
            return &s[..i];
        }
    }
    s
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

    let text = String::from("Rust lifetimes are compile-time regions, not runtime durations.");
    let excerpt = Excerpt { source: &text };
    println!("excerpt = {}", use_excerpt(excerpt));
}
