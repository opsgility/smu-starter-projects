// EXPECTED ERROR: E0515 — cannot return reference to local variable `s`
// HINT: `greet` builds a local `String s` and returns `&s`. The local is
//       dropped at the end of the function — the reference would dangle.
//       Fix: return the owned String. Change `-> &str` to `-> String` and
//       return `s` by value (not `&s`).
// FIX ME: Make this compile.

fn greet(name: &str) -> &str {
    let s = format!("Hello, {name}!");
    &s
}

fn main() {
    println!("{}", greet("Mira"));
}
