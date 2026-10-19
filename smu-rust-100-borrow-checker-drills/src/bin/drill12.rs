// FIX ME: Make this program compile and print `hello, drill 12` then `drill 12 passed`.
// EXPECTED ERROR: E0308 — mismatched types (expected `String`, found `&str`)
// Hint: the string literal `"drill 12"` has type `&str`, not `String`. The
//       `greet` function wants an owned `String`. Convert at the `let` site
//       with `.to_string()` or `String::from(...)`.

fn greet(name: String) {
    println!("hello, {name}");
}

fn main() {
    let name: String = "drill 12";
    greet(name);
    println!("drill 12 passed");
}
