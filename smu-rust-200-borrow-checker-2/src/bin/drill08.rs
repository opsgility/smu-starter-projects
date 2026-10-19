// EXPECTED ERROR: E0515 cannot return reference to local variable `s`
// (closely related to E0597 — returning &str from a locally owned String)
// HINT: `greet` builds a local `String s` and tries to return `&s` as `&str`.
//       The local goes out of scope at the end of greet(), so the reference
//       would dangle. Two fixes:
//         (a) return the owned `String` (change signature to `-> String`)
//         (b) take a `&str` input, don't build a local, return a slice of it
//             (requires lifetime annotation; Course 2 Lesson 6 covers this)

fn greet(name: &str) -> &str {
    let s = format!("Hello, {name}!");
    // FIX ME: s is owned by this function. Returning &s makes a reference that
    //         outlives its owner. Change the signature to -> String and return s.
    &s
}

fn main() {
    let g = greet("Mira");
    println!("{g}");
}
